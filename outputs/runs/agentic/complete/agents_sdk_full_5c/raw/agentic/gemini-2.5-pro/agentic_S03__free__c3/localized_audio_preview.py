import os
from elevenlabs.client import ElevenLabs

def generate_audio_preview(text: str, voice_id: str = "pNInz6obpgDQGcFmaJgB") -> bytes:
    """
    Generates a spoken audio preview of translated text using ElevenLabs.

    Args:
        text: The translated text to convert to speech.
        voice_id: The ID of the ElevenLabs voice to use. Defaults to "Rachel".

    Returns:
        The raw audio data in bytes.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)

    audio = client.generate(
        text=text,
        voice=voice_id,
        model="eleven_multilingual_v2"
    )

    if isinstance(audio, bytes):
        return audio
    
    # Handle potential generator response
    audio_bytes = b"".join([chunk for chunk in audio])
    return audio_bytes
