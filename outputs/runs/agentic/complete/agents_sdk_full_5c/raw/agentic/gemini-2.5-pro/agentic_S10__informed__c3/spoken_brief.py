import os
from elevenlabs.client import ElevenLabs

def generate_speech(text: str) -> bytes:
    """
    Generates speech from text using the ElevenLabs API.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

    client = ElevenLabs(api_key=api_key)
    
    audio = client.generate(
        text=text,
        voice="Rachel",
        model="eleven_multilingual_v2"
    )
    
    if isinstance(audio, bytes):
        return audio
        
    # The SDK can also return an iterator of chunks
    audio_bytes = b"".join(chunk for chunk in audio)
    return audio_bytes
