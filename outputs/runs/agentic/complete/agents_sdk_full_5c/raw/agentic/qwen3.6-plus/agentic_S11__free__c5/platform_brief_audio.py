"""
[LATER-STEP] Generate spoken briefings from platform outputs using Azure OpenAI
text-to-speech capabilities.

Uses the Azure OpenAI tts-1 or tts-1-hd deployment to synthesize audio
from platform-generated text content, producing natural-sounding spoken
briefings for evaluation, accessibility, or presentation purposes.
"""

from __future__ import annotations

from typing import Optional

from openai import AzureOpenAI

from model_models import SpeechResult
from model_client import get_azure_openai_client


# Azure OpenAI TTS deployment names
AZURE_TTS_DEPLOYMENT_STANDARD = "tts-1"
AZURE_TTS_DEPLOYMENT_HD = "tts-1-hd"

# Supported Azure OpenAI TTS voices
AZURE_TTS_VOICES = [
    "alloy",
    "echo",
    "fable",
    "onyx",
    "nova",
    "shimmer",
]


def platform_brief_audio(
    text: str,
    voice: str = "nova",
    deployment_name: str = AZURE_TTS_DEPLOYMENT_STANDARD,
    response_format: str = "mp3",
    speed: float = 1.0,
    client: Optional[AzureOpenAI] = None,
) -> SpeechResult:
    """
    Generate a spoken audio briefing from platform output text using Azure OpenAI TTS.

    Synthesizes natural speech from the provided text content using the
    Azure OpenAI text-to-speech deployment (tts-1 or tts-1-hd).

    Args:
        text: The text content to convert to speech.
        voice: TTS voice name. Options: alloy, echo, fable, onyx, nova, shimmer.
               Defaults to 'nova'.
        deployment_name: Azure OpenAI TTS deployment name.
                         Defaults to 'tts-1'.
        response_format: Audio output format. Supported: 'mp3', 'wav', 'opus', 'aac'.
                         Defaults to 'mp3'.
        speed: Speech speed multiplier. Range 0.25 to 4.0. Defaults to 1.0.
        client: Optional pre-configured AzureOpenAI client.

    Returns:
        SpeechResult with binary audio data and provider metadata.
    """
    if client is None:
        client = get_azure_openai_client()

    if not text.strip():
        raise ValueError("Input text for audio generation cannot be empty")

    if voice not in AZURE_TTS_VOICES:
        raise ValueError(
            f"Invalid voice '{voice}'. Supported Azure OpenAI TTS voices: "
            f"{', '.join(AZURE_TTS_VOICES)}"
        )

    # Clamp speed to Azure OpenAI supported range
    clamped_speed = max(0.25, min(4.0, speed))

    # Validate response format
    valid_formats = ["mp3", "wav", "opus", "aac"]
    if response_format not in valid_formats:
        response_format = "mp3"

    response = client.audio.speech.create(
        model=deployment_name,
        voice=voice,
        input=text,
        response_format=response_format,
        speed=clamped_speed,
    )

    # Azure OpenAI speech response provides audio as raw bytes via content() or read()
    audio_bytes = response.content

    model_id = getattr(response, "model", deployment_name)

    return SpeechResult(
        audio_data=audio_bytes,
        model_id=model_id,
        deployment_name=deployment_name,
        voice_name=voice,
        format=response_format,
        raw_response=response,
    )


def platform_brief_audio_from_response(
    response_content: str,
    voice: str = "nova",
    deployment_name: str = AZURE_TTS_DEPLOYMENT_HD,
    response_format: str = "mp3",
    client: Optional[AzureOpenAI] = None,
) -> SpeechResult:
    """
    Generate spoken audio briefing from a platform model response string.

    Convenience wrapper that takes the raw text output from a prior
    Azure OpenAI chat completion and converts it to speech.

    Args:
        response_content: Text content from a previous platform model response.
        voice: TTS voice to use for the briefing.
        deployment_name: Azure OpenAI TTS deployment (hd recommended for briefings).
        response_format: Audio format for the output.
        client: Optional pre-configured AzureOpenAI client.

    Returns:
        SpeechResult with the generated audio briefing.
    """
    return platform_brief_audio(
        text=response_content,
        voice=voice,
        deployment_name=deployment_name,
        response_format=response_format,
        client=client,
    )


def platform_brief_audio_batch(
    texts: list[str],
    voice: str = "nova",
    deployment_name: str = AZURE_TTS_DEPLOYMENT_STANDARD,
    response_format: str = "mp3",
    speed: float = 1.0,
    client: Optional[AzureOpenAI] = None,
) -> list[SpeechResult]:
    """
    Generate spoken audio briefings for multiple platform outputs.

    Creates separate audio files for each text input, suitable for
    multi-section briefings or chapter-based audio content.

    Args:
        texts: List of text strings to convert to speech.
        voice: TTS voice for all briefings.
        deployment_name: Azure OpenAI TTS deployment.
        response_format: Audio output format.
        speed: Speech speed multiplier.
        client: Optional pre-configured AzureOpenAI client.

    Returns:
        List of SpeechResult objects, one per input text.
    """
    results = []
    for text in texts:
        if text.strip():
            result = platform_brief_audio(
                text=text,
                voice=voice,
                deployment_name=deployment_name,
                response_format=response_format,
                speed=speed,
                client=client,
            )
            results.append(result)
    return results
