import os
from elevenlabs.client import ElevenLabs

def generate_audio_briefing(text: str) -> bytes:
    """
    Generates a spoken briefing from text using the ElevenLabs API.

    Args:
        text: The text to convert to speech.

    Returns:
        The audio data as bytes.
    """
    api_key = os.getenv("ELEVEN_API_KEY")
    if not api_key:
        raise ValueError("ELEVEN_API_KEY environment variable not set.")
    
    # Provider-specific client class
    client = ElevenLabs(api_key=api_key)

    # The generate method is part of the ElevenLabs SDK and calls their API.
    # Provider-specific model/voice ID
    audio = client.generate(
        text=text,
        voice="Rachel",
        model="eleven_multilingual_v2"
    )

    # The SDK returns a generator, so we concatenate the chunks
    audio_bytes = b"".join(chunk for chunk in audio)
    
    return audio_bytes
