import os
from typing import Optional
from elevenlabs import generate, set_api_key

def generate_spoken_brief(
    text: str,
    voice: str = "Rachel",
    model: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
) -> bytes:
    """
    Generate a spoken brief from text using ElevenLabs Text-to-Speech.
    
    Args:
        text: Input text to convert to speech.
        voice: Voice identifier (e.g., "Rachel", "Adam").
        model: TTS model identifier.
        output_format: Audio format (e.g., "mp3_44100_128").
    
    Returns:
        Audio data as bytes.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY environment variable not set.")
    
    set_api_key(api_key)
    audio = generate(
        text=text,
        voice=voice,
        model=model,
        output_format=output_format,
    )
    return audio