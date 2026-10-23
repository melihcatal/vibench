"""
Synthesize plain text to an audio byte stream using Amazon Polly.

This module provides text-to-speech synthesis functionality that converts
plain text input into an audio byte stream via the Amazon Polly service.

Provider: Amazon Polly (polly.us-east-1.amazonaws.com)
Model/Voice: Configurable Polly voice IDs (e.g., Joanna, Matthew, Salli)
"""

from typing import Optional

from speech_client import PollyClient, get_polly_client
from speech_models import (
    SynthesisRequest,
    SynthesisResponse,
    OutputFormat,
    TextType,
    normalize_voice_id,
)


def synthesize_text_to_audio(
    text: str,
    voice_id: str = "Joanna",
    language_code: str = "en-US",
    output_format: str = "mp3",
    client: Optional[PollyClient] = None,
) -> SynthesisResponse:
    """
    Synthesize plain text to audio using Amazon Polly.
    
    Args:
        text: Plain text to synthesize (max 3000 characters for Polly)
        voice_id: Amazon Polly voice ID (e.g., 'Joanna', 'Matthew', 'Salli')
        language_code: BCP-47 language code for voice selection
        output_format: Audio output format ('mp3', 'ogg_vorbis', 'pcm')
        client: Optional pre-configured PollyClient instance
        
    Returns:
        SynthesisResponse containing the audio byte stream and metadata
        
    Raises:
        ValueError: If text exceeds Amazon Polly character limit
        Exception: If Polly API call fails
    """
    if len(text) > 3000:
        raise ValueError(
            "Text exceeds Amazon Polly limit of 3000 characters. "
            "Use synthesize_ssml with long-form support or split text."
        )
    
    # Normalize voice for the specified locale
    normalized_voice = normalize_voice_id(voice_id, language_code)
    
    request = SynthesisRequest(
        text=text,
        voice_id=normalized_voice,
        output_format=OutputFormat(output_format),
        text_type=TextType.TEXT,
        language_code=language_code,
    )
    
    polly = client or get_polly_client()
    
    response = polly.synthesize_speech(
        text=text,
        voice_id=normalized_voice,
        output_format=output_format,
        text_type="text",
        language_code=language_code,
    )
    
    return SynthesisResponse.from_polly_response(response, voice_id=normalized_voice)


def synthesize_text_stream(
    text: str,
    voice_id: str = "Joanna",
    output_format: str = "mp3",
) -> bytes:
    """
    Synthesize text and return raw audio bytes.
    
    Convenience function for direct byte stream access.
    Uses Amazon Polly with the specified voice (e.g., Joanna, Matthew).
    
    Args:
        text: Text to synthesize
        voice_id: Amazon Polly voice identifier
        output_format: Output audio format
        
    Returns:
        Raw audio bytes from Amazon Polly AudioStream
    """
    response = synthesize_text_to_audio(
        text=text,
        voice_id=voice_id,
        output_format=output_format,
    )
    return response.audio_stream


if __name__ == "__main__":
    sample_text = "Hello, this is a demonstration of Amazon Polly text-to-speech synthesis."
    result = synthesize_text_to_audio(sample_text, voice_id="Joanna")
    print(f"Synthesized {len(result.audio_stream)} bytes using voice {result.voice_id}")
    print(f"Content-Type: {result.content_type}")
    print(f"Request ID: {result.request_id}")
