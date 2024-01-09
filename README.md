# TTS-AI

This project is created using: https://github.com/rhasspy/piper


# Exemplos de requisição:
- /segmentar-audio
    params:
      {
        "texto": "Olá #NOME# Um passarinho acabou de me contar que você fez cadastro na plataforma #PLATAFORMA# estamos muito felizes em ter você como o mais novo #STATUS#",
        "voz": "pt_BR-faber-medium"
      }

- /juntar-audio
    params:
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
                    "#PLATAFORMA#": "Disparo Pro",
                    "#STATUS#": "cliente"
                }
           ]
        }

  - /audio-unico
      params:
        {
            "texto": "Olá #NOME# Um passarinho acabou de me contar que você fez cadastro na plataforma #PLATAFORMA# estamos muito felizes em ter você como o mais novo #STATUS#",
            "voz": "pt_BR-faber-medium",
            "substituicoes": [
                {
                    "#NOME#": "Tainam",
                    "#PLATAFORMA#": "Disparo Pro",
                    "#STATUS#": "cliente"
                }
           ]
        }
