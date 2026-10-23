import os
from elevenlabs.client import ElevenLabs

def generate_audio_brief(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> bytes:
    """
    Generates a spoken audio brief from retrieved search results text.

    Args:
        text: The text to convert to speech.
        voice_id: The ID of the ElevenLabs voice to use (default is "Rachel").

    Returns:
        The audio data as a bytes object.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    
    client = ElevenLabs(api_key=api_key)
    
    # The 'generate' method streams audio chunks. We concatenate them.
    audio_stream = client.generate(
        text=text,
        voice=voice_id,
        model="eleven_multilingual_v2"
    )
    
    audio_bytes = b"".join(chunk for chunk in audio_stream)
    return audio_bytes
