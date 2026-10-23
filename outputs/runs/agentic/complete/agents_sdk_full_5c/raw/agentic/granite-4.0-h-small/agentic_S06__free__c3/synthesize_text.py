# synthesize_text.py
# [SAME-SCENARIO]
# Uses Google Cloud Text-to-Speech API to synthesize plain text into an audio byte stream.

import os
from google.cloud import texttospeech

# Helper utilities from same-scenario local files
from speech_client import TextToSpeechClient
from speech_models import TextToSpeechResponse

def synthesize(text: str, language_code: str = "en-US", voice_name: str = None) -> bytes:
    """Synthesize plain text to an audio byte stream.
    Args:
        text: The plain text to synthesize.
        language_code: BCP-47 language identifier (default en-US).
        voice_name: Optional specific voice ID (e.g., "en-US-Wavenet-D").
    Returns:
        Binary audio data in MP3 format.
    """
    # Construct the client (uses GOOGLE_APPLICATION_CREDENTIALS env var)
    client = TextToSpeechClient()
    # Select voice if not provided
    if not voice_name:
        voice_name = select_voice(language_code)[0]  # fall back to first voice
    # Text-to-speech configuration
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    # Send request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    # Validate response
    resp = TextToSpeechResponse(response)
    resp.validate()
    # Return raw audio bytes
    return response.audio_content
