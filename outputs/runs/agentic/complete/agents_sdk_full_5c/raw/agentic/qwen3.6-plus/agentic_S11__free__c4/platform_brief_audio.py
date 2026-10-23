"""Generate spoken briefings from platform outputs.

Provider: Azure AI Speech (https://learn.microsoft.com/azure/ai-services/speech-service/)
SDK: azure-cognitiveservices-speech >= 1.30.0 with SpeechConfig, SpeechSynthesizer.
Uses the Azure AI Speech SDK with concrete neural voice identifiers to synthesize
spoken audio from platform model text outputs.
"""

from __future__ import annotations

import os
from io import BytesIO
from typing import Optional

import azure.cognitiveservices.speech as speechsdk

from model_models import PlatformResponse


# Azure AI Speech provider-specific configuration
_AZURE_SPEECH_KEY_ENV = "AZURE_SPEECH_KEY"
_AZURE_SPEECH_REGION_ENV = "AZURE_SPEECH_REGION"

# Azure AI Speech neural voice identifiers (provider-specific)
AZURE_NEURAL_VOICES = {
    "en-US": "en-US-JennyNeural",
    "en-GB": "en-GB-SoniaNeural",
    "es-ES": "es-ES-ElviraNeural",
    "fr-FR": "fr-FR-DeniseNeural",
    "de-DE": "de-DE-KatjaNeural",
    "ja-JP": "ja-JP-NanamiNeural",
    "zh-CN": "zh-CN-XiaoxiaoNeural",
    "pt-BR": "pt-BR-FranciscaNeural",
    "it-IT": "it-IT-ElsaNeural",
    "ko-KR": "ko-KR-SunHiNeural",
}


def resolve_speech_key() -> str:
    """Return the Azure AI Speech API key from environment."""
    key = os.environ.get(_AZURE_SPEECH_KEY_ENV)
    if not key:
        raise RuntimeError(
            f"Missing provider environment variable: {_AZURE_SPEECH_KEY_ENV}"
        )
    return key


def resolve_speech_region() -> str:
    """Return the Azure AI Speech region from environment."""
    region = os.environ.get(_AZURE_SPEECH_REGION_ENV)
    if not region:
        raise RuntimeError(
            f"Missing provider environment variable: {_AZURE_SPEECH_REGION_ENV}"
        )
    return region


def build_speech_config(
    *,
    api_key: Optional[str] = None,
    region: Optional[str] = None,
) -> speechsdk.SpeechConfig:
    """Build a provider-specific Azure AI Speech configuration.

    Args:
        api_key: Azure Speech API key. Resolved from env if not provided.
        region: Azure Speech region. Resolved from env if not provided.

    Returns:
        Configured SpeechConfig.
    """
    resolved_key = api_key or resolve_speech_key()
    resolved_region = region or resolve_speech_region()

    config = speechsdk.SpeechConfig(
        subscription=resolved_key,
        region=resolved_region,
    )
    return config


def get_voice_for_locale(locale: str) -> str:
    """Return the Azure neural voice identifier for a given locale.

    Args:
        locale: BCP-47 locale code (e.g., 'en-US', 'es-ES').

    Returns:
        Azure neural voice name (e.g., 'en-US-JennyNeural').

    Raises:
        ValueError: If the locale has no configured Azure neural voice.
    """
    if locale not in AZURE_NEURAL_VOICES:
        raise ValueError(
            f"No Azure neural voice configured for locale '{locale}'. "
            f"Available: {', '.join(AZURE_NEURAL_VOICES.keys())}"
        )
    return AZURE_NEURAL_VOICES[locale]


def platform_brief_audio(
    *,
    text: str,
    voice_name: Optional[str] = None,
    locale: Optional[str] = "en-US",
    output_format: Optional[str] = None,
    api_key: Optional[str] = None,
    region: Optional[str] = None,
    speech_config: Optional[speechsdk.SpeechConfig] = None,
) -> bytes:
    """Generate spoken audio briefing from platform model output text.

    Uses the Azure AI Speech SDK to synthesize text into audio using a
    neural voice. Supports multiple output formats including WAV, MP3,
    and OGG.

    Azure neural voices like 'en-US-JennyNeural' provide high-quality
    natural-sounding speech synthesis.

    Args:
        text: The model output text to convert to speech.
        voice_name: Azure neural voice name. If None, defaults to locale's configured voice.
        locale: BCP-47 locale for voice selection. Used when voice_name is None.
        output_format: Azure speech output format string.
            Options: 'riff-24khz-16bit-mono-pcm', 'audio-24khz-48kbitrate-mono-mp3',
            'audio-24khz-96kbps-mono-mp3', 'audio-48khz-192kbps-mono-mp3',
            'ogg-24khz-16bit-mono-opus'.
        api_key: Azure Speech API key. Resolved from env if not provided.
        region: Azure Speech region. Resolved from env if not provided.
        speech_config: Pre-built SpeechConfig. Built automatically if not provided.

    Returns:
        Audio data as bytes in the requested format.
    """
    if speech_config is None:
        speech_config = build_speech_config(api_key=api_key, region=region)

    if output_format:
        speech_config.set_speech_synthesis_output_format(output_format)

    resolved_voice = voice_name or get_voice_for_locale(locale or "en-US")
    speech_config.speech_synthesis_voice_name = resolved_voice

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=None,  # No file output — capture to memory
    )

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data

    cancellation = speechsdk.SpeechSynthesisCancellationDetails.from_result(result)
    raise RuntimeError(
        f"Azure AI Speech synthesis failed: {cancellation.reason} - {cancellation.error_details}"
    )


def platform_brief_audio_to_file(
    *,
    text: str,
    filepath: str,
    voice_name: Optional[str] = None,
    locale: Optional[str] = "en-US",
    output_format: Optional[str] = None,
    api_key: Optional[str] = None,
    region: Optional[str] = None,
    speech_config: Optional[speechsdk.SpeechConfig] = None,
) -> str:
    """Generate spoken audio briefing and save directly to a file.

    Uses Azure AudioConfig to write the synthesized audio to disk without
    loading the full audio into memory.

    Args:
        text: The model output text to convert to speech.
        filepath: Output audio file path.
        voice_name: Azure neural voice name.
        locale: BCP-47 locale for voice selection.
        output_format: Azure speech output format string.
        api_key: Azure Speech API key.
        region: Azure Speech region.
        speech_config: Pre-built SpeechConfig.

    Returns:
        The filepath where audio was saved.
    """
    if speech_config is None:
        speech_config = build_speech_config(api_key=api_key, region=region)

    if output_format:
        speech_config.set_speech_synthesis_output_format(output_format)

    resolved_voice = voice_name or get_voice_for_locale(locale or "en-US")
    speech_config.speech_synthesis_voice_name = resolved_voice

    audio_config = speechsdk.audio.AudioOutputConfig(filename=filepath)
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config,
    )

    result = synthesizer.speak_text_async(text).get()

    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        cancellation = speechsdk.SpeechSynthesisCancellationDetails.from_result(result)
        raise RuntimeError(
            f"Azure AI Speech synthesis failed: {cancellation.reason} - {cancellation.error_details}"
        )

    return filepath


def platform_response_to_brief_audio(
    *,
    platform_response: PlatformResponse,
    voice_name: Optional[str] = None,
    locale: Optional[str] = "en-US",
    output_format: Optional[str] = "audio-24khz-48kbitrate-mono-mp3",
    api_key: Optional[str] = None,
    region: Optional[str] = None,
    speech_config: Optional[speechsdk.SpeechConfig] = None,
) -> bytes:
    """Convert a PlatformResponse content into spoken audio.

    Args:
        platform_response: The PlatformResponse from the model platform.
        voice_name: Azure neural voice name.
        locale: BCP-47 locale for voice selection.
        output_format: Azure speech output format.
        api_key: Azure Speech API key.
        region: Azure Speech region.
        speech_config: Pre-built SpeechConfig.

    Returns:
        Audio data as bytes.
    """
    return platform_brief_audio(
        text=platform_response.content,
        voice_name=voice_name,
        locale=locale,
        output_format=output_format,
        api_key=api_key,
        region=region,
        speech_config=speech_config,
    )


def generate_ssml_briefing(
    *,
    text: str,
    voice_name: Optional[str] = None,
    locale: Optional[str] = "en-US",
    rate: str = "+0%",
    volume: str = "default",
    api_key: Optional[str] = None,
    region: Optional[str] = None,
    speech_config: Optional[speechsdk.SpeechConfig] = None,
) -> bytes:
    """Generate spoken briefing with SSML control over rate, volume, and prosody.

    Azure AI Speech supports SSML (Speech Synthesis Markup Language) for fine-grained
    control over voice output including speaking rate, volume, and pitch.

    Args:
        text: The text to synthesize.
        voice_name: Azure neural voice name.
        locale: BCP-47 locale for SSML language attribute.
        rate: Speaking rate adjustment (e.g., '+20%', '-10%').
        volume: Volume level (e.g., 'loud', 'soft', 'default', or '+10dB').
        api_key: Azure Speech API key.
        region: Azure Speech region.
        speech_config: Pre-built SpeechConfig.

    Returns:
        Audio data as bytes.
    """
    if speech_config is None:
        speech_config = build_speech_config(api_key=api_key, region=region)

    resolved_voice = voice_name or get_voice_for_locale(locale or "en-US")
    resolved_locale = locale or "en-US"

    ssml = (
        f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        f'xml:lang="{resolved_locale}">'
        f'<voice name="{resolved_voice}">'
        f'<prosody rate="{rate}" volume="{volume}">'
        f'{text}'
        f'</prosody>'
        f'</voice>'
        f'</speak>'
    )

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=None,
    )

    result = synthesizer.speak_ssml_async(ssml).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data

    cancellation = speechsdk.SpeechSynthesisCancellationDetails.from_result(result)
    raise RuntimeError(
        f"Azure AI Speech SSML synthesis failed: {cancellation.reason} - {cancellation.error_details}"
    )
