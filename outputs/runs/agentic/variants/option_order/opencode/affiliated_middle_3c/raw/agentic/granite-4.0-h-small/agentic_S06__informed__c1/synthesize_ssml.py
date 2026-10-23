import os
import sys
from google.cloud import texttospeech  # provider: Cloud Text-to-Speech

from speech_client import TextToSpeechClient
from speech_models import SynthesisConfig

def synthesize_ssml(ssml: str, voice_name: str = None, language_code: str = 'en-US', prosody: dict = None) -> bytes:
    """Synthesize SSML text to audio with optional voice and prosody controls.

    Args:
        ssml (str): SSML formatted text.
        voice_name (str, optional): Specific voice name (e.g., 'en-US-Wavenet-D').
        language_code (str, optional): Language code (e.g., 'en-US').
        prosody (dict, optional): Dictionary of prosody attributes like rate, pitch, volume.

    Returns:
        bytes: Synthesized audio bytes in MP3 format.
    """
    # Build SynthesisConfig with SSML support
    config = SynthesisConfig(
        input_ssml=ssml,
        voice_name=voice_name,
        language_code=language_code,
        audio_encoding=texttospeech.AudioEncoding.MP3,
        prosody=prosody
    )
    # Authenticated client via GOOGLE_APPLICATION_CREDENTIALS
    client = TextToSpeechClient()
    audio_bytes = client.synthesize_speech(config=config)
    return audio_bytes

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: synthesize_ssml.py '<speak>Hello <break time=\"500ms\"/> world!</speak>' [voice_name] [language_code] ["""{\"rate\":0.9}""" ]")
        sys.exit(1)
    ssml = sys.argv[1]
    voice_name = sys.argv[2] if len(sys.argv) > 2 else None
    language_code = sys.argv[3] if len(sys.argv) > 3 else 'en-US'
    prosody_opt = sys.argv[4] if len(sys.argv) > 4 else '{}'
    import json
    prosody = json.loads(prosody_opt) if prosody_opt else None
    audio = synthesize_ssml(ssml, voice_name, language_code, prosody)
    print(f"Audio generated ({len(audio)} bytes)")
