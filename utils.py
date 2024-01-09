from pydub import AudioSegment
from datetime import datetime
from config import PG_CONFIG
from zipfile import ZipFile
import subprocess
import re
import base64
import psycopg2
import speech_recognition as sr
import os


def gerar_arquivo_base64(arquivo):
    with open(arquivo, 'rb') as file:
        file_binary_data = file.read()

    base64_encoded = base64.b64encode(file_binary_data)
    base64_string = base64_encoded.decode('utf-8')

    return base64_string


def inserir_audio_base64(nome, arquivo):
    try:
        pg_connection = psycopg2.connect(**PG_CONFIG)
        arquivobase64 = gerar_arquivo_base64(arquivo)
        pg_cursor = pg_connection.cursor()
        pg_cursor.execute(
                "INSERT INTO ssm_audio_processed (name, image_data) VALUES (%s, %s) RETURNING id", (nome, arquivobase64))
        return pg_cursor.fetchone()
    except psycopg2.Error as e:
        return False


def criar_audio_segmentado(texto_segmentado, indice_segmentado, modelo_voz, data_e_hora_formatada):
    comando = f'echo {texto_segmentado} | piper --model ./{modelo_voz}.onnx --output_file {modelo_voz}_{data_e_hora_formatada}_{indice_segmentado}.wav'
    caminho_arquivo = f'./{modelo_voz}_{data_e_hora_formatada}_{indice_segmentado}.wav'

    try:
        subprocess.run(comando, shell=True, check=True)
        inserir_audio_base64(f'{modelo_voz}_{data_e_hora_formatada}_{indice_segmentado}.wav',
                             caminho_arquivo)
        return caminho_arquivo
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
        return None


def segmentar_texto(texto_original):
    partes = re.split(r'#\w+#', texto_original)
    return [parte for parte in partes if parte != '']


def juntar_audios(lista_de_arquivos, lista_de_arquivos_segmentados, modelo_voz):
    segmentos = []

    for arquivo, arquivo_segmentado in zip(lista_de_arquivos, lista_de_arquivos_segmentados):
        segmentos.append('./' + arquivo)
        segmentos.append('./' + arquivo_segmentado)

    data_e_hora_formatada = datetime.now().strftime("%Y%m%d%H%M%S")
    string_list = ' '.join(segmentos)
    comando = f' sox {string_list} {modelo_voz}_{data_e_hora_formatada}.wav'
    caminho_arquivo = f'./{modelo_voz}_{data_e_hora_formatada}.wav'
    print(caminho_arquivo)
    try:
        subprocess.run(comando, shell=True, check=True)
        inserir_audio_base64(f'{modelo_voz}_{data_e_hora_formatada}.wav',
                             caminho_arquivo)
        return caminho_arquivo
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
        return None


def estender_audio(audio_cortado):
    name = audio_cortado
    audio_cortado = AudioSegment.from_file(audio_cortado)
    duracao_atual = len(audio_cortado)
    duracao_alvo = duracao_atual * 2
    silencio_necessario = duracao_alvo - duracao_atual
    while len(audio_cortado) < duracao_alvo:
        silencio = AudioSegment.silent(duration=silencio_necessario)
        # Repetir a parte cortada até atingir a duração alvo
        audio_cortado += silencio
    # Cortar o áudio estendido para a duração exata
    audio_estendido = audio_cortado[:duracao_alvo]
    audio_estendido.export(f"{name.split('/')[1]}", format="wav")
    return f"{name.split('/')[1]}"


def cortar_audio_antes_da_palavra(arquivo_audio, palavra_alvo, modelo_voz):
    # Carregar o áudio
    print("Entrou ")
    audio = AudioSegment.from_file(arquivo_audio)

    # Converter para texto usando reconhecimento de fala
    recognizer = sr.Recognizer()
    with sr.AudioFile(arquivo_audio) as source:
        record = recognizer.record(source, duration=audio.duration_seconds)
        audio_texto = recognizer.recognize_google(record, language='pt-BR')
    # Encontrar a posição da palavra alvo
    posicao_palavra = audio_texto.find(palavra_alvo)
    if posicao_palavra != -1:
        duracao_segundos = len(audio) / 1000
        duracao_milissegundos = int(duracao_segundos * 1000)

        # Cortar áudio antes da palavra alvo
        tempo_corte = posicao_palavra * duracao_milissegundos  # Convertendo posição para milissegundos
        start_time = (posicao_palavra * 67) - (67 * len(palavra_alvo))
        end_time = posicao_palavra * 67
        # Extract the chunk from the original audio
        audio_cortado = audio[start_time:end_time]
        audio_cortado = estender_audio(audio_cortado)
        # Salvar o áudio cortado
        data_e_hora_formatada = datetime.now().strftime("%Y%m%d%H%M%S")
        audio_cortado.export(f"{modelo_voz}_{data_e_hora_formatada}.wav", format="wav")
        print(f"Áudio cortado antes da palavra '{palavra_alvo}' salvo como '{modelo_voz}_{data_e_hora_formatada}.wav'")
        return f"{modelo_voz}_{data_e_hora_formatada}.wav"
    else:
        return False


def export_to_zip(modelo_voz, audio):
    data_e_hora_formatada = datetime.now().strftime("%Y%m%d%H%M%S")
    zip_temporario = os.path.join('./', f'{modelo_voz}_{data_e_hora_formatada}.zip')
    with ZipFile(zip_temporario, 'w') as zipe:
        for indice, segmento in enumerate(audio):
            zipe.write(segmento, os.path.basename(segmento))
    return zip_temporario
