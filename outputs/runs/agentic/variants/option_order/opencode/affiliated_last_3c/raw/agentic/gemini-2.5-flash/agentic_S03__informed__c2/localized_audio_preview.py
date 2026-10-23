import os
from google.cloud import texttospeech  # Provider-identifying signal
from translation_models import AudioPreviewRequest, AudioPreviewResponse

# Google Cloud Text-to-Speech client initialization
client = texttospeech.TextToSpeechClient()


def generate_audio_preview(request: AudioPreviewRequest) -> AudioPreviewResponse:
    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code, name=request.voice_name
    )

    audio_encoding = texttospeech.AudioEncoding.MP3
    if request.audio_format.lower() == "ogg_opus":
        audio_encoding = texttospeech.AudioEncoding.OGG_OPUS
    elif request.audio_format.lower() == "wav":
        audio_encoding = texttospeech.AudioEncoding.LINEAR16

    audio_config = texttospeech.AudioConfig(audio_encoding=audio_encoding)

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return AudioPreviewResponse(audio_content=response.audio_content)
