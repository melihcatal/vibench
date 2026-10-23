import os
import requests
from elevenlabs_sdk import ElevenLabs, Voice

# ElevenLabs Text-to-Speech integration
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)


def generate_spoken_preview(text: str, voice_id: str = "110053") -> bytes:
    """Create an audio file (bytes) representing spoken translated text.

    Uses the ElevenLabs TTS service and returns raw MP3 data.
    """
    voice = Voice.from_id(voice_id)
    response = client.text_to_speech(
        input=text, model="eleven_monolingual_v1", voice=voice, audio_format="mp3"
    )
    # ElevenLabs returns audio as base64-encoded string in 'audio'
    if "error" in response:
        raise RuntimeError(f"TTS failed: {response['error']}")
    # Return raw MP3 bytes
    return response["audio"].encode("utf-8")
