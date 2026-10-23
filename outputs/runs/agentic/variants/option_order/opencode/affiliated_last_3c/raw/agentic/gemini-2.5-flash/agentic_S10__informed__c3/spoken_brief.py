import os
from google.cloud import texttospeech
from model_models import TextToSpeechRequest, TextToSpeechResponse


def generate_spoken_brief(request: TextToSpeechRequest) -> TextToSpeechResponse:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code, name=request.voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return TextToSpeechResponse(audio_content=response.audio_content)
