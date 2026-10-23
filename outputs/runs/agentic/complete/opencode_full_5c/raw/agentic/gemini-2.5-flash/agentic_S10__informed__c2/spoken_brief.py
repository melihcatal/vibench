import os
from google.cloud import texttospeech

from model_models import SynthesizeSpeechRequest, SynthesizeSpeechResponse


def generate_spoken_brief(
    text: str, voice_name: str = "en-US-Standard-C", language_code: str = "en-US"
) -> SynthesizeSpeechResponse:
    """Generates a spoken brief from the model output using Google Cloud Text-to-Speech."""
    # Google Cloud Text-to-Speech client will use GOOGLE_APPLICATION_CREDENTIALS for authentication
    # Make sure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or authentication is handled by gcloud cli

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return SynthesizeSpeechResponse(audio_content=response.audio_content)
