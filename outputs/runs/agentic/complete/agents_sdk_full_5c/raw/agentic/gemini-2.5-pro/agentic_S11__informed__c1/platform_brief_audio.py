import os
from elevenlabs import generate, set_api_key

def generate_audio_briefing(text: str) -> bytes:
    """
    Generates a spoken briefing from platform output text using ElevenLabs.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    
    set_api_key(api_key)

    audio = generate(
        text=text,
        voice="Rachel",
        model="eleven_multilingual_v2"
    )
    
    if isinstance(audio, bytes):
        return audio
    
    # Handle iterator if audio is streamed
    audio_bytes = b"".join(chunk for chunk in audio)
    return audio_bytes
