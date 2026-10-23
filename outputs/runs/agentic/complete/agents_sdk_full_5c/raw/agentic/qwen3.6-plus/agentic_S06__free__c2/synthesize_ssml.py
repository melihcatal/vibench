"""
Synthesize SSML with voice and prosody controls using Amazon Polly.

This module provides SSML-based text-to-speech synthesis with fine-grained
control over voice characteristics, prosody, emphasis, and pacing via
Amazon Polly's SSML support.

Provider: Amazon Polly (polly.us-east-1.amazonaws.com)
SSML Version: 1.0 with Amazon-specific extensions (amazon:domain, amazon:effect)
"""

from typing import Optional

from speech_client import PollyClient, get_polly_client
from speech_models import (
    SSMLSynthesisRequest,
    SynthesisResponse,
    OutputFormat,
    TextType,
    normalize_voice_id,
    build_ssml,
)


def synthesize_ssml_to_audio(
    text: str,
    voice_id: str = "Joanna",
    language_code: str = "en-US",
    output_format: str = "mp3",
    rate: Optional[str] = None,
    pitch: Optional[str] = None,
    volume: Optional[str] = None,
    emphasis_level: Optional[str] = None,
    break_duration: Optional[str] = None,
    use_conversational: bool = False,
    client: Optional[PollyClient] = None,
) -> SynthesisResponse:
    """
    Synthesize SSML to audio using Amazon Polly.
    
    Args:
        text: Plain text or raw SSML to synthesize
        voice_id: Amazon Polly voice ID (e.g., 'Joanna', 'Matthew', 'Ivy')
        language_code: BCP-47 language code
        output_format: Audio output format ('mp3', 'ogg_vorbis', 'pcm')
        rate: Speaking rate ('slow', 'fast', 'x-slow', '150%')
        pitch: Pitch adjustment ('+10%', '-1st', 'high', 'low')
        volume: Volume level ('loud', 'soft', '-6dB', '+3dB')
        emphasis_level: Emphasis strength ('strong', 'moderate', 'reduced')
        break_duration: Pause duration ('500ms', '1s', '250ms')
        use_conversational: Use Amazon Polly conversational domain
        client: Optional pre-configured PollyClient
        
    Returns:
        SynthesisResponse with audio stream and metadata
    """
    normalized_voice = normalize_voice_id(voice_id, language_code)
    
    # Build SSML if text is not already wrapped
    if not text.strip().startswith('<speak>'):
        ssml = build_ssml(
            text=text,
            voice_name=voice_id if use_conversational else None,
            rate=rate,
            pitch=pitch,
            volume=volume,
            emphasis_level=emphasis_level,
            break_duration=break_duration,
        )
    else:
        ssml = text
    
    polly = client or get_polly_client()
    
    response = polly.synthesize_speech(
        text=ssml,
        voice_id=normalized_voice,
        output_format=output_format,
        text_type="ssml",
        language_code=language_code,
    )
    
    return SynthesisResponse.from_polly_response(response, voice_id=normalized_voice)


def synthesize_with_prosody(
    text: str,
    voice_id: str = "Joanna",
    rate: str = "medium",
    pitch: str = "medium",
    volume: str = "medium",
    output_format: str = "mp3",
) -> bytes:
    """
    Synthesize text with explicit prosody controls via Amazon Polly SSML.
    
    Args:
        text: Text to synthesize
        voice_id: Amazon Polly voice ID
        rate: Speaking rate ('x-slow', 'slow', 'medium', 'fast', 'x-fast', or percentage)
        pitch: Pitch ('x-low', 'low', 'medium', 'high', 'x-high', or semitone shift)
        volume: Volume ('silent', 'x-soft', 'soft', 'medium', 'loud', 'x-loud', or dB)
        output_format: Audio format
        
    Returns:
        Raw audio bytes from Amazon Polly
    """
    ssml = build_ssml(
        text=text,
        rate=rate if rate != "medium" else None,
        pitch=pitch if pitch != "medium" else None,
        volume=volume if volume != "medium" else None,
    )
    
    response = synthesize_ssml_to_audio(
        text=ssml,
        voice_id=voice_id,
        output_format=output_format,
    )
    return response.audio_stream


def synthesize_with_emphasis(
    text: str,
    voice_id: str = "Joanna",
    emphasis_text: Optional[str] = None,
    emphasis_level: str = "strong",
    break_after: Optional[str] = "500ms",
) -> bytes:
    """
    Synthesize text with emphasized portions using Amazon Polly SSML.
    
    Args:
        text: Base text to synthesize
        emphasis_text: Specific substring to emphasize (if None, emphasizes entire text)
        emphasis_level: 'strong', 'moderate', or 'reduced'
        break_after: Pause duration after emphasized text
        
    Returns:
        Raw audio bytes from Amazon Polly
    """
    if emphasis_text and emphasis_text in text:
        # Wrap the emphasis text with <emphasis> tags
        parts = text.split(emphasis_text, 1)
        ssml = build_ssml(
            text=parts[0] + emphasis_text,
            emphasis_level=emphasis_level,
            break_duration=break_after,
        )
        # Add remaining text after break
        if len(parts) > 1 and parts[1]:
            ssml = ssml.replace('</speak>', f'{parts[1]}</speak>')
    else:
        ssml = build_ssml(
            text=text,
            emphasis_level=emphasis_level,
            break_duration=break_after,
        )
    
    response = synthesize_ssml_to_audio(text=ssml, voice_id=voice_id)
    return response.audio_stream


if __name__ == "__main__":
    sample = "Welcome to our product demonstration."
    result = synthesize_ssml_to_audio(
        sample,
        voice_id="Joanna",
        rate="slow",
        pitch="+10%",
        volume="loud",
    )
    print(f"Generated {len(result.audio_stream)} bytes of SSML audio")
