import os
from google.cloud import texttospeech
from model_models import TextToSpeechRequest, TextToSpeechResponse


def generate_spoken_brief(request: TextToSpeechRequest) -> TextToSpeechResponse:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name,
    )

    audio_encoding_map = {
        "MP3": texttospeech.AudioEncoding.MP3,
        "LINEAR16": texttospeech.AudioEncoding.LINEAR16,
        "OGG_OPUS": texttospeech.AudioEncoding.OGG_OPUS,
    }

    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding_map.get(
            request.audio_encoding, texttospeech.AudioEncoding.MP3
        )
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return TextToSpeechResponse(audio_content=response.audio_content)
