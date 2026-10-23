# [LATER-STEP] localized_audio_preview.py

import os
import tempfile
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from google.cloud import texttospeech


def generate_audio_preview(translated_text, voice="en-US-Standard-B"):
    """Create a spoken preview of translated text using Google Cloud Text-to-Speech.

    Args:
        translated_text (str): Text to be turned into speech.
        voice (str): Google TTS voice code (default: 'en-US-Standard-B').

    Returns:
        dict: Path to a temporary WAV file containing the spoken audio and provider metadata.
    """
    client = (
        texttospeech.TextToSpeechClient()
    )  # uses GOOGLE_APPLICATION_CREDENTIALS env var
    input_ssml = texttospeech.SynthesisInput(ssml=f"<speak>{translated_text}</speak>")
    voice_params = texttospeech.VoiceSelectionParams(language_code="en-US", name=voice)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    response = client.synthesize_speech(
        input=input_ssml, voice=voice_params, audio_config=audio_config
    )
    audio_bytes = response.audio_content

    # Store in a temporary file (not deleted automatically so caller can retrieve)
    fd, path = tempfile.mkstemp(suffix=".wav", prefix="tts_")
    with os.fdopen(fd, "wb") as f:
        f.write(audio_bytes)

    return {
        "audio_path": path,
        "provider": "Google Cloud Text-to-Speech",
        "model_id": "localized_audio_preview",
    }
