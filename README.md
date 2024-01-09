# TTS-AI

This project was created using: https://github.com/rhasspy/piper

Supported Voices: https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0

The words that are between ## will be replaced by the array of substitutions sent in the request parameters.

# Exemplos de requisição:
## /segmentar-audio
```json
      {
        "texto": "Olá #NOME# Um passarinho acabou de me contar que você fez cadastro na plataforma #PLATAFORMA# estamos muito felizes em ter você como o mais novo #STATUS#",
        "voz": "pt_BR-faber-medium"
      }

```
Retorna um zip com os audios segmentados.
- /juntar-audio
```json
        {
            "texto": "Olá #NOME# Um passarinho acabou de me contar que você fez cadastro na plataforma #PLATAFORMA# estamos muito felizes em ter você como o mais novo #STATUS#",
            "voz": "pt_BR-faber-medium",
            "nome": [
                "pt_BR-faber-medium_20240109152218_1.wav",
                "pt_BR-faber-medium_20240109152218_2.wav",
                "pt_BR-faber-medium_20240109152218_3.wav"
            ],
            "substituicoes": [
                {
                    "#NOME#": "Tainam",
                    "#PLATAFORMA#": "TESTE",
                    "#STATUS#": "cliente"
                }
           ]
        }
```
Retorna um zip com os audios juntados das N substituições.
- /audio-unico
```json
        {
            "texto": "Olá #NOME# Um passarinho acabou de me contar que você fez cadastro na plataforma #PLATAFORMA# estamos muito felizes em ter você como o mais novo #STATUS#",
            "voz": "pt_BR-faber-medium",
            "substituicoes": [
                {
                    "#NOME#": "Tainam",
                    "#PLATAFORMA#": "TESTE",
                    "#STATUS#": "cliente"
                }
           ]
        }
```
Retorna um zip com os audios das N substituições.
