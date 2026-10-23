import os
from typing import Optional
from elevenlabs import generate, save
from model_models import ModelOutputWithMetadata


def generate_elevenlabs_audio(
    text: str,
    voice: str = "Rachel",
    api_key: Optional[str] = None,
) -> bytes:
    """
    Generate spoken audio from text using ElevenLabs TTS.
    
    Args:
        text: Input text to convert to speech.
        voice: Voice ID or name (e.g., "Rachel").
        api_key: ElevenLabs API key. Defaults to environment variable.
    
    Returns:
        Audio data as bytes.
    """
    audio = generate(text=text, voice=voice, api_key=api_key or os.getenv("ELEVENLABS_API_KEY"))
    return audio


def create_platform_brief_audio(
    output_with_metadata: ModelOutputWithMetadata,
    voice: str = "Rachel",
    api_key: Optional[str] = None,
    output_path: Optional[str] = None,
) -> Optional[bytes]:
    """
    Generate spoken briefings from platform model outputs.
    
    Args:
        output_with_metadata: Model output and metadata.
        voice: Voice ID or name (e.g., "Rachel").
        api_key: ElevenLabs API key. Defaults to environment variable.
        output_path: Optional path to save audio file. If provided, saves to disk.
    
    Returns:
        Audio data as bytes if output_path is None, else None.
    """
    audio = generate_elevenlabs_audio(
        output_with_metadata.output,
        voice=voice,
        api_key=api_key,
    )
    
    if output_path:
        save(audio, filename=output_path)
        return None
    
    return audio