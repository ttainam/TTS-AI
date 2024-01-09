from utils import segmentar_texto, criar_audio_segmentado, juntar_audios, estender_audio, export_to_zip
from flask import Flask, request, jsonify, send_file
from datetime import datetime
from zipfile import ZipFile
import os

app = Flask(__name__)


@app.route('/segmentar-audio', methods=['POST'])
def segmentar():
    try:
        data = request.get_json()
        texto_original = data.get('texto')
        modelo_voz = data.get('voz')

        if texto_original is None or modelo_voz is None:
            return jsonify({'erro': 'Texto ou voz ausentes'})

        data_e_hora_formatada = datetime.now().strftime("%Y%m%d%H%M%S")
        texto_segmentado = segmentar_texto(texto_original)
        audios_segmentados = []

        zip_temporario = os.path.join('./', f'{modelo_voz}_{data_e_hora_formatada}.zip')

        with ZipFile(zip_temporario, 'w') as zip:
            for indice, segmento in enumerate(texto_segmentado):
                audio_segmentado = criar_audio_segmentado(segmento, indice + 1, modelo_voz, data_e_hora_formatada)
                audios_segmentados.append(audio_segmentado)
                zip.write(audio_segmentado, os.path.basename(audio_segmentado))

        response = send_file(zip_temporario, as_attachment=True, download_name=f'{modelo_voz}_{data_e_hora_formatada}.zip')
        os.unlink(zip_temporario)
        return response

    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/juntar-audio', methods=['POST'])
def juntar():
    data = request.get_json()
    texto_original = data.get('texto')
    modelo_voz = data.get('voz')
    nome = data.get('nome')
    substituicoes = data.get('substituicoes')

    if texto_original is None or modelo_voz is None:
        return jsonify({'erro': 'Texto ou voz ausentes'})

    audios_segmentados = []
    audio = []

    for indice, substituicao in enumerate(substituicoes):
        i = indice + 1
        for chave, valor in substituicao.items():
            data_e_hora_formatada = datetime.now().strftime("%Y%m%d%H%M%S")
            audio_segmentado = (
                criar_audio_segmentado(valor, i, modelo_voz, data_e_hora_formatada))
            audio_segmentado = estender_audio(audio_segmentado)
            audios_segmentados.append(audio_segmentado)
            i += 1
        i += 1
        audio_final = juntar_audios(nome, audios_segmentados, modelo_voz)
        audio.append(audio_final)
        audios_segmentados = []

    data_e_hora_formatada = datetime.now().strftime("%Y%m%d%H%M%S")
    zip_temporario = os.path.join('./', f'{modelo_voz}_{data_e_hora_formatada}.zip')
    with ZipFile(zip_temporario, 'w') as zipe:
        for indice, segmento in enumerate(audio):
            zipe.write(segmento, os.path.basename(segmento))

    response = send_file(zip_temporario, as_attachment=True, download_name=f'{modelo_voz}_{data_e_hora_formatada}.zip')
    os.unlink(zip_temporario)
    return response


@app.route('/audio-unico', methods=['POST'])
def unico():
    data = request.get_json()
    texto_original = data.get('texto')
    modelo_voz = data.get('voz')
    substituicoes = data.get('substituicoes')

    if texto_original is None or modelo_voz is None:
        return jsonify({'erro': 'Texto ou voz ausentes'})
    audio = []
    data_e_hora_formatada = datetime.now().strftime("%Y%m%d%H%M%S")
    for indice, substituicao in enumerate(substituicoes):
        audio_segmentado = ''
        i = indice + 1
        texto_modificado = texto_original
        for chave, valor in substituicao.items():
            texto_modificado = texto_modificado.replace(chave, valor)
        audio_segmentado = criar_audio_segmentado(texto_modificado, i, modelo_voz, data_e_hora_formatada)
        audio.append(audio_segmentado)
        i += 1

    zip_temporario = export_to_zip(modelo_voz, audio)
    data_e_hora_formatada = datetime.now().strftime("%Y%m%d%H%M%S")
    response = send_file(zip_temporario, as_attachment=True, download_name=f'{modelo_voz}_{data_e_hora_formatada}.zip')
    os.unlink(zip_temporario)
    return response


if __name__ == '__main__':
    app.run(debug=True)