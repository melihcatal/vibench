from elevenlabs import generate, set_api_key
import os
from typing import Dict, Any


def generate_audio_brief(text: str, voice: str = "Rachel") -> Dict[str, Any]:
    """Generate spoken briefing from text using ElevenLabs TTS."""
    set_api_key(os.getenv("ELEVENLABS_API_KEY"))
    
    audio = generate(
        text=text,
        voice=voice,
        model="eleven_multilingual_v2"
    )
    
    return {
        "audio": audio,
        "voice": voice,
        "text": text
    }