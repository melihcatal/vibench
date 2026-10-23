import os
from elevenlabs.client import ElevenLabs

def generate_audio_preview(text: str, voice_id: str = "Rachel") -> bytes:
    """
    Generates a spoken audio preview of translated copy using ElevenLabs API.
    
    Expects ELEVENLABS_API_KEY environment variable.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not found in environment variables.")

    client = ElevenLabs(api_key=api_key)
    
    # Generate audio
    audio_data = client.generate(
        text=text,
        voice=voice_id,
        model="eleven_multilingual_v2"
    )
    
    # The SDK returns a generator, so we concatenate the chunks
    audio_bytes = b"".join(audio_data)
    
    return audio_bytes
