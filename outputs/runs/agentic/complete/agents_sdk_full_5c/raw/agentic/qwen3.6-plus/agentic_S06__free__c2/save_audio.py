"""
Write synthesized speech audio to a local file or object using Amazon Polly.

This module handles persisting audio byte streams from Amazon Polly synthesis
to local files with proper format handling and metadata.

Provider: Amazon Polly (polly.us-east-1.amazonaws.com)
Audio Formats: mp3, ogg_vorbis, pcm
"""

import os
from pathlib import Path
from typing import Optional, Union

from speech_client import PollyClient, get_polly_client
from speech_models import SynthesisResponse, OutputFormat
from synthesize_text import synthesize_text_to_audio


# File extension mapping for Amazon Polly output formats
FORMAT_EXTENSIONS = {
    "mp3": ".mp3",
    "ogg_vorbis": ".ogg",
    "pcm": ".pcm",
    OutputFormat.MP3: ".mp3",
    OutputFormat.OGG_VORBIS: ".ogg",
    OutputFormat.PCM: ".pcm",
}

# Content-Type mapping for Amazon Polly responses
CONTENT_TYPE_MAP = {
    "audio/mpeg": ".mp3",
    "audio/ogg": ".ogg",
    "audio/x-wav": ".pcm",
}


def save_audio_to_file(
    audio_bytes: bytes,
    output_path: Union[str, Path],
    content_type: Optional[str] = None,
    output_format: Optional[str] = None,
) -> Path:
    """
    Save Amazon Polly audio bytes to a local file.
    
    Args:
        audio_bytes: Raw audio bytes from Polly AudioStream
        output_path: Destination file path
        content_type: MIME type from Polly response (e.g., 'audio/mpeg')
        output_format: Format override ('mp3', 'ogg_vorbis', 'pcm')
        
    Returns:
        Path to the saved file
    """
    output_path = Path(output_path)
    
    # Determine extension
    if not output_path.suffix:
        if output_format:
            ext = FORMAT_EXTENSIONS.get(output_format, ".mp3")
        elif content_type:
            ext = CONTENT_TYPE_MAP.get(content_type, ".mp3")
        else:
            ext = ".mp3"
        output_path = output_path.with_suffix(ext)
    
    # Ensure parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write audio bytes
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    
    return output_path


def synthesize_and_save(
    text: str,
    output_path: Union[str, Path],
    voice_id: str = "Joanna",
    language_code: str = "en-US",
    output_format: str = "mp3",
    client: Optional[PollyClient] = None,
) -> dict:
    """
    Synthesize text with Amazon Polly and save to file.
    
    Args:
        text: Text to synthesize
        output_path: Destination file path
        voice_id: Amazon Polly voice ID
        language_code: BCP-47 language code
        output_format: Audio output format
        client: Optional pre-configured PollyClient
        
    Returns:
        Dict with synthesis and save metadata
    """
    # Synthesize using Amazon Polly
    response = synthesize_text_to_audio(
        text=text,
        voice_id=voice_id,
        language_code=language_code,
        output_format=output_format,
        client=client,
    )
    
    # Save to file
    saved_path = save_audio_to_file(
        audio_bytes=response.audio_stream,
        output_path=output_path,
        content_type=response.content_type,
        output_format=output_format,
    )
    
    return {
        "file_path": str(saved_path),
        "file_size": saved_path.stat().st_size,
        "voice_id": response.voice_id,
        "format": output_format,
        "request_id": response.request_id,
        "characters_used": len(text),
    }


def save_synthesis_response(
    response: SynthesisResponse,
    output_path: Union[str, Path],
) -> Path:
    """
    Save a SynthesisResponse from Amazon Polly to a local file.
    
    Args:
        response: SynthesisResponse containing Polly audio data
        output_path: Destination file path
        
    Returns:
        Path to the saved file
    """
    return save_audio_to_file(
        audio_bytes=response.audio_stream,
        output_path=output_path,
        content_type=response.content_type,
        output_format=response.output_format,
    )


if __name__ == "__main__":
    sample_text = "This audio was synthesized by Amazon Polly and saved to disk."
    result = synthesize_and_save(
        sample_text,
        output_path="output/sample.mp3",
        voice_id="Joanna",
    )
    print(f"Saved {result['file_size']} bytes to {result['file_path']}")
    print(f"Voice: {result['voice_id']}, Request ID: {result['request_id']}")
