import os
from google.cloud import texttospeech
from translation_models import AudioPreviewRequest, AudioPreviewResponse


def generate_spoken_preview(request: AudioPreviewRequest) -> AudioPreviewResponse:
    """
    Generates spoken previews of translated copy using Google Cloud Text-to-Speech.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name,
    )

    audio_encoding_map = {
        "LINEAR16": texttospeech.AudioEncoding.LINEAR16,
        "MP3": texttospeech.AudioEncoding.MP3,
        "OGG_OPUS": texttospeech.AudioEncoding.OGG_OPUS,
        # Add other supported formats as needed
    }
    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding_map.get(
            request.audio_format.upper(), texttospeech.AudioEncoding.LINEAR16
        )
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return AudioPreviewResponse(
        audio_content=response.audio_content,
        audio_format=request.audio_format,  # Return the requested format
    )
