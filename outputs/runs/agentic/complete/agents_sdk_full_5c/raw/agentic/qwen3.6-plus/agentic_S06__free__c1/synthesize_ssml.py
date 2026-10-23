"""
synthesize_ssml.py - Synthesizes SSML with voice and prosody controls using ElevenLabs.

Provider: ElevenLabs (https://api.elevenlabs.io)
Model: eleven_multilingual_v2 (supports SSML prosody tags)
SDK: elevenlabs Python package
"""

from typing import Optional

from elevenlabs import generate
from elevenlabs.client import ElevenLabs

from speech_client import get_elevenlabs_client, validate_audio_format, validate_voice_id
from speech_models import SSMLRequest, TTSResponse


# ElevenLabs model supporting SSML
ELEVEN_MULTILINGUAL_V2 = "eleven_multilingual_v2"

# Default ElevenLabs voice ID (Rachel)
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"


def synthesize_ssml(
    raw_text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: str = ELEVEN_MULTILINGUAL_V2,
    output_format: str = "mp3_44100_128",
    pitch: Optional[str] = None,
    rate: Optional[str] = None,
    volume: Optional[str] = None,
    emphasis_level: Optional[str] = None,
    break_before: Optional[str] = None,
    break_after: Optional[str] = None,
    stability: float = 0.5,
    similarity: float = 0.75,
    style: float = 0.0,
    api_key: Optional[str] = None,
) -> TTSResponse:
    """Synthesize SSML-formatted speech using ElevenLabs.

    Builds an SSML string with prosody, emphasis, and break controls,
    then sends it to the ElevenLabs API for synthesis.

    ElevenLabs supports SSML prosody tags for pitch, rate, and volume
    adjustments, as well as break and emphasis tags.

    Args:
        raw_text: Plain text to be wrapped in SSML.
        voice_id: ElevenLabs voice ID.
        model_id: ElevenLabs model ID (must support SSML).
        output_format: ElevenLabs audio format.
        pitch: Pitch adjustment (e.g., '+10%', '-5%', 'x-high').
        rate: Speaking rate (e.g., '1.2', 'slow', 'fast').
        volume: Volume level (e.g., '+3dB', 'loud', 'soft').
        emphasis_level: Emphasis strength ('strong', 'moderate', 'reduced').
        break_before: Pause before text (e.g., '500ms', '2s').
        break_after: Pause after text (e.g., '500ms', '2s').
        stability: Voice stability (0.0 - 1.0).
        similarity: Voice similarity boost (0.0 - 1.0).
        style: Style exaggeration (0.0 - 1.0).
        api_key: Optional explicit API key override.

    Returns:
        TTSResponse containing audio bytes and metadata.
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("Input text cannot be empty.")

    validate_voice_id(voice_id)
    validate_audio_format(output_format)

    ssml_req = SSMLRequest(
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format,
        stability=stability,
        similarity=similarity,
        style=style,
    )

    # Build SSML with prosody controls
    ssml_text = ssml_req.build_ssml(
        raw_text=raw_text,
        pitch=pitch,
        rate=rate,
        volume=volume,
        emphasis_level=emphasis_level,
        break_duration=break_before,
    )

    # Append trailing break if specified
    if break_after:
        # Insert break before closing </speak>
        ssml_text = ssml_text.replace("</speak>", f'<break time="{break_after}"/></speak>')

    client = get_elevenlabs_client(api_key=api_key)

    audio_bytes = generate(
        text=ssml_text,
        voice=voice_id,
        model=model_id,
        output_format=output_format,
        voice_settings={
            "stability": stability,
            "similarity_boost": similarity,
            "style": style,
            "use_speaker_boost": True,
        },
    )

    if isinstance(audio_bytes, bytes):
        raw_audio = audio_bytes
    else:
        raw_audio = b"".join(audio_bytes) if hasattr(audio_bytes, '__iter__') else bytes(audio_bytes)

    return TTSResponse(
        audio_bytes=raw_audio,
        content_type="audio/mpeg",
        model_id=model_id,
        voice_id=voice_id,
        character_count=len(raw_text),
    )


def synthesize_ssml_with_emphasis(
    text: str,
    emphasized_words: list,
    voice_id: str = DEFAULT_VOICE_ID,
    api_key: Optional[str] = None,
) -> TTSResponse:
    """Synthesize text with specific words emphasized.

    Wraps specified words in <emphasis level="strong"> SSML tags.

    Args:
        text: The full text to synthesize.
        emphasized_words: List of words to emphasize.
        voice_id: ElevenLabs voice ID.
        api_key: Optional explicit API key override.

    Returns:
        TTSResponse with emphasized audio.
    """
    emphasized_text = text
    for word in emphasized_words:
        emphasized_text = emphasized_text.replace(
            word,
            f'<emphasis level="strong">{word}</emphasis>'
        )

    return synthesize_ssml(
        raw_text=emphasized_text,
        voice_id=voice_id,
        api_key=api_key,
    )


def synthesize_ssml_with_pauses(
    text: str,
    pause_positions: list,
    pause_duration: str = "500ms",
    voice_id: str = DEFAULT_VOICE_ID,
    api_key: Optional[str] = None,
) -> TTSResponse:
    """Synthesize text with pauses inserted at specific word positions.

    Args:
        text: The full text to synthesize.
        pause_positions: List of word indices where pauses should be inserted.
        pause_duration: Duration of each pause (e.g., '500ms', '1s').
        voice_id: ElevenLabs voice ID.
        api_key: Optional explicit API key override.

    Returns:
        TTSResponse with paused audio.
    """
    words = text.split()
    pause_tag = f' <break time="{pause_duration}"/> '
    for idx in sorted(pause_positions, reverse=True):
        if 0 <= idx < len(words):
            words.insert(idx + 1, pause_tag.strip())

    ssml_content = " ".join(words)
    return synthesize_ssml(
        raw_text=ssml_content,
        voice_id=voice_id,
        api_key=api_key,
    )


if __name__ == "__main__":
    sample_text = "Welcome to our presentation today."
    response = synthesize_ssml(
        sample_text,
        pitch="+5%",
        rate="0.9",
        emphasis_level="moderate",
        break_before="300ms",
    )
    print(f"Synthesized SSML: {response.character_count} characters.")
    print(f"Audio size: {len(response.audio_bytes)} bytes")
    print(f"Model: {response.model_id}")
