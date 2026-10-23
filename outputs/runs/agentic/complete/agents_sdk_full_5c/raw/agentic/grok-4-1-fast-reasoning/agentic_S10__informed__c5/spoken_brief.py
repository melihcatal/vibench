import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from elevenlabs.commons import AudioOutputFormat
import io

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY must be set.")

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def generate_spoken_brief(text: str, voice_id: str = "pNInz6obpgDQGcFmaJgB") -> bytes:
    """Generate spoken brief audio from text using ElevenLabs TTS."""
    audio = client.generate(
        text=text,
        voice=voice_id,
        model="eleven_monolingual_v1",
        output_format=AudioOutputFormat.MP3_44100_128
    )
    return audio