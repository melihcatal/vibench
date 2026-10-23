"""Generate spoken briefings from platform outputs using OpenAI Text-to-Speech.

Uses the OpenAI Audio/Speech API with the tts-1-hd model to convert
text outputs from managed model platforms into high-quality spoken
audio briefings.
"""

from typing import Dict, Any, Optional

from model_client import load_platform_config, get_openai_client
from model_models import AudioBriefingResult


OPENAI_TTS_MODEL = "tts-1-hd"
OPENAI_TTS_VOICE = "alloy"
OPENAI_TTS_RESPONSE_FORMAT = "mp3"


def generate_spoken_briefing(
    text: str,
    voice: Optional[str] = None,
    model: Optional[str] = None,
    response_format: str = "mp3",
    speed: float = 1.0,
    provider_config: Optional[Dict[str, Any]] = None,
) -> AudioBriefingResult:
    """Generate a spoken audio briefing from platform model output.

    Uses the OpenAI Text-to-Speech API to convert text into spoken
    audio using the tts-1-hd model for high-quality voice synthesis.

    Args:
        text: The text content to convert to speech.
        voice: Voice identifier (alloy, echo, fable, onyx, nova, shimmer).
        model: TTS model override (tts-1 or tts-1-hd).
        response_format: Audio format (mp3, opus, aac, flac).
        speed: Speech speed multiplier (0.25 to 4.0).
        provider_config: Optional pre-loaded OpenAI configuration.

    Returns:
        AudioBriefingResult with audio data and metadata.
    """
    if provider_config is None:
        provider_config = load_platform_config("openai")

    model_id = model or provider_config.get("tts_model", OPENAI_TTS_MODEL)
    voice_id = voice or provider_config.get("tts_voice", OPENAI_TTS_VOICE)
    client = get_openai_client(provider_config)

    response = client.audio.speech.create(
        model=model_id,
        voice=voice_id,
        input=text,
        response_format=response_format,
        speed=speed,
    )

    audio_bytes = response.content

    return AudioBriefingResult(
        text=text,
        audio_data=audio_bytes,
        audio_format=response_format,
        model=model_id,
        voice=voice_id,
        provider="openai",
    )


def generate_briefing_to_file(
    text: str,
    output_path: str,
    voice: Optional[str] = None,
    model: Optional[str] = None,
    provider_config: Optional[Dict[str, Any]] = None,
) -> AudioBriefingResult:
    """Generate a spoken briefing and save directly to a file.

    Args:
        text: The text content to convert to speech.
        output_path: File path to save the audio output.
        voice: Voice identifier override.
        model: TTS model override.
        provider_config: Optional pre-loaded configuration.

    Returns:
        AudioBriefingResult with audio data and metadata.
    """
    if provider_config is None:
        provider_config = load_platform_config("openai")

    model_id = model or provider_config.get("tts_model", OPENAI_TTS_MODEL)
    voice_id = voice or provider_config.get("tts_voice", OPENAI_TTS_VOICE)
    client = get_openai_client(provider_config)

    response = client.audio.speech.create(
        model=model_id,
        voice=voice_id,
        input=text,
        response_format="mp3",
    )

    response.stream_to_file(output_path)

    return AudioBriefingResult(
        text=text,
        audio_data=b"",
        audio_format="mp3",
        model=model_id,
        voice=voice_id,
        provider="openai",
    )


def generate_briefings_batch(
    texts: list,
    voice: Optional[str] = None,
    model: Optional[str] = None,
    provider_config: Optional[Dict[str, Any]] = None,
) -> list:
    """Generate spoken briefings for multiple platform outputs.

    Args:
        texts: List of text outputs to convert to speech.
        voice: Voice identifier override.
        model: TTS model override.
        provider_config: Optional pre-loaded configuration.

    Returns:
        List of AudioBriefingResult objects.
    """
    results = []
    for text in texts:
        result = generate_spoken_briefing(
            text=text,
            voice=voice,
            model=model,
            provider_config=provider_config,
        )
        results.append(result)
    return results


def get_available_voices(
    provider_config: Optional[Dict[str, Any]] = None,
) -> list:
    """Get list of available OpenAI TTS voices.

    Args:
        provider_config: Optional pre-loaded configuration.

    Returns:
        List of voice identifier strings.
    """
    return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


def get_tts_model_info(
    provider_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Get information about the configured TTS model.

    Args:
        provider_config: Optional pre-loaded configuration.

    Returns:
        Dictionary with TTS model metadata.
    """
    if provider_config is None:
        provider_config = load_platform_config("openai")

    model_id = provider_config.get("tts_model", OPENAI_TTS_MODEL)

    return {
        "model": model_id,
        "voices": get_available_voices(),
        "supported_formats": ["mp3", "opus", "aac", "flac"],
        "max_characters": 4096,
        "provider": "openai",
    }
