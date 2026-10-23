"""Generate spoken briefings from platform outputs using Azure AI Speech TTS.

Uses Azure AI Speech TTS service (sdk=azure-cognitiveservices-speech) with
AZURE_SPEECH_KEY and AZURE_SPEECH_REGION.
"""

from __future__ import annotations

import io
import os
from dataclasses import dataclass
from typing import Optional

import azure.cognitiveservices.speech as speechsdk


@dataclass
class AudioBriefingResult:
    """Result of Azure AI Speech text-to-speech conversion."""

    input_text: str
    audio_data: bytes
    voice_name: str
    language: str
    output_format: str
    duration_ms: int = 0
    raw_result: Optional[speechsdk.SpeechSynthesisResult] = None


_SPEECH_KEY_ENV = "AZURE_SPEECH_KEY"
_SPEECH_REGION_ENV = "AZURE_SPEECH_REGION"
_DEFAULT_VOICE = "en-US-AriaNeural"
_DEFAULT_OUTPUT_FORMAT = speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm


def _get_speech_key() -> str:
    key = os.environ.get(_SPEECH_KEY_ENV, "")
    if not key:
        raise ValueError(f"{_SPEECH_KEY_ENV} environment variable is not set")
    return key


def _get_speech_region() -> str:
    region = os.environ.get(_SPEECH_REGION_ENV, "")
    if not region:
        raise ValueError(f"{_SPEECH_REGION_ENV} environment variable is not set")
    return region


def _create_speech_config(
    voice_name: str = _DEFAULT_VOICE,
    output_format: speechsdk.SpeechSynthesisOutputFormat = _DEFAULT_OUTPUT_FORMAT,
) -> speechsdk.SpeechConfig:
    """Create an Azure AI Speech config for TTS synthesis."""
    speech_config = speechsdk.SpeechConfig(
        subscription=_get_speech_key(),
        region=_get_speech_region(),
    )
    speech_config.speech_synthesis_voice_name = voice_name
    speech_config.set_speech_synthesis_output_format(output_format)
    return speech_config


def _format_briefing_text(
    platform_output: str,
    title: Optional[str] = None,
    include_intro: bool = True,
) -> str:
    """Format platform model output into a spoken briefing script."""
    parts = []
    if title:
        parts.append(f"Here is your briefing on: {title}.")
    if include_intro and not title:
        parts.append("Here is your briefing.")
    parts.append(platform_output)
    parts.append("End of briefing.")
    return " ".join(parts)


def platform_brief_audio(
    platform_output: str,
    voice_name: str = _DEFAULT_VOICE,
    title: Optional[str] = None,
    language: str = "en-US",
    include_intro: bool = True,
    output_format: speechsdk.SpeechSynthesisOutputFormat = _DEFAULT_OUTPUT_FORMAT,
) -> AudioBriefingResult:
    """Generate a spoken audio briefing from platform model output text.

    Uses Azure AI Speech TTS to synthesize audio from the provided text.
    The input text is optionally formatted with an intro and title.

    Args:
        platform_output: The model-generated text to convert to speech.
        voice_name: Azure Neural TTS voice name (e.g., en-US-AriaNeural).
        title: Optional briefing title prepended to the spoken text.
        language: Language code (e.g., en-US).
        include_intro: Whether to prepend a spoken intro phrase.
        output_format: Azure Speech output audio format.

    Returns:
        AudioBriefingResult with audio bytes and synthesis metadata.
    """
    briefing_text = _format_briefing_text(
        platform_output,
        title=title,
        include_intro=include_intro,
    )

    speech_config = _create_speech_config(
        voice_name=voice_name,
        output_format=output_format,
    )

    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=None,
    )

    result = speech_synthesizer.speak_text_async(briefing_text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_bytes = result.audio_data
        audio_duration = 0
        if hasattr(result, "audio_duration"):
            audio_duration = result.audio_duration
        elif hasattr(result, "duration"):
            audio_duration = result.duration
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        raise RuntimeError(
            f"Speech synthesis canceled: {cancellation.reason}. "
            f"Error details: {cancellation.error_details}"
        )
    else:
        raise RuntimeError(
            f"Speech synthesis failed with reason: {result.reason}"
        )

    return AudioBriefingResult(
        input_text=briefing_text,
        audio_data=audio_bytes,
        voice_name=voice_name,
        language=language,
        output_format=output_format.name if hasattr(output_format, "name") else str(output_format),
        duration_ms=audio_duration,
        raw_result=result,
    )


def platform_brief_audio_to_file(
    platform_output: str,
    output_path: str,
    voice_name: str = _DEFAULT_VOICE,
    title: Optional[str] = None,
    language: str = "en-US",
    include_intro: bool = True,
) -> AudioBriefingResult:
    """Generate a spoken briefing and write audio directly to a WAV file.

    Args:
        platform_output: The model-generated text to convert to speech.
        output_path: File path for the output audio file.
        voice_name: Azure Neural TTS voice name.
        title: Optional briefing title.
        language: Language code.
        include_intro: Whether to prepend a spoken intro.

    Returns:
        AudioBriefingResult with synthesis metadata.
    """
    briefing_text = _format_briefing_text(
        platform_output,
        title=title,
        include_intro=include_intro,
    )

    speech_config = _create_speech_config(
        voice_name=voice_name,
        output_format=_DEFAULT_OUTPUT_FORMAT,
    )

    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_path)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config,
    )

    result = speech_synthesizer.speak_text_async(briefing_text).get()

    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        cancellation = result.cancellation_details
        raise RuntimeError(
            f"Speech synthesis canceled: {cancellation.reason}. "
            f"Error details: {cancellation.error_details}"
        )

    return AudioBriefingResult(
        input_text=briefing_text,
        audio_data=b"",
        voice_name=voice_name,
        language=language,
        output_format=_DEFAULT_OUTPUT_FORMAT.name,
        raw_result=result,
    )


if __name__ == "__main__":
    result = platform_brief_audio(
        platform_output="Managed model platforms enable scalable AI deployment with enterprise security.",
        voice_name="en-US-AriaNeural",
        title="AI Platform Overview",
    )
    print(f"Voice: {result.voice_name}")
    print(f"Audio size: {len(result.audio_data)} bytes")
    print(f"Format: {result.output_format}")
