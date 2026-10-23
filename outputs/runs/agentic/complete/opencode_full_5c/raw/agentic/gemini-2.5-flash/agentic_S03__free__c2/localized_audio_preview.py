from google.cloud import texttospeech
from translation_models import (
    LocalizedAudioPreviewRequest,
    LocalizedAudioPreviewResponse,
)
import os


def generate_audio_preview(
    request: LocalizedAudioPreviewRequest,
) -> LocalizedAudioPreviewResponse:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language,
        name=request.voice_name,  # Example: 'en-US-Wavenet-D'
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
    )

    # The audio content is binary
    return LocalizedAudioPreviewResponse(audio_content=response.audio_content)


# Provider-identifying signal: google.cloud.texttospeech import
