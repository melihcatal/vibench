import os
from typing import Optional
from elevenlabs import generate, set_api_key


def generate_spoken_brief(
    text: str,
    voice_id: str = "EXAVITQu4vr4xnSDxMaL",
    model_id: str = "eleven_multilingual_v2"
) -> Optional[bytes]:
    """
    Generate a spoken brief from the model output using ElevenLabs.
    
    Args:
        text: Text to convert to speech.
        voice_id: ElevenLabs voice identifier.
        model_id: ElevenLabs TTS model identifier.
        
    Returns:
        Audio bytes or None if failed.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        return None

    set_api_key(api_key)
    try:
        audio = generate(
            text=text,
            voice=voice_id,
            model=model_id
        )
        return audio
    except Exception:
        return None