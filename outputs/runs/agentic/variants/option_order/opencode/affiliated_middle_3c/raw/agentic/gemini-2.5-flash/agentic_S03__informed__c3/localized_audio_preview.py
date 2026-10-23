import os
from google.cloud import texttospeech


def generate_audio_preview(
    text: str, language_code: str, voice_name: str = "en-US-Wavenet-D"
) -> bytes:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # to the path of your service account key file for authentication.

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
