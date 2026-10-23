"""Synthesize SSML with voice and prosody controls using Azure AI Speech TTS."""

import os
from typing import Optional

import azure.cognitiveservices.speech as speechsdk

from speech_client import get_azure_speech_config
from speech_models import TTSRequest, TTSResponse


def synthesize_ssml(
    ssml: str,
    api_key: Optional[str] = None,
    region: Optional[str] = None,
) -> TTSResponse:
    """Synthesize SSML markup to audio using Azure AI Speech TTS.

    The SSML should contain <speak> root element with voice, prosody,
    and other Speech Synthesis Markup Language controls.

    Args:
        ssml: A complete SSML document string starting with <speak>.
        api_key: Azure Speech key. Falls back to AZURE_SPEECH_KEY env var.
        region: Azure Speech region. Falls back to AZURE_SPEECH_REGION env var.

    Returns:
        TTSResponse containing the synthesized audio bytes.
    """
    speech_config = get_azure_speech_config(api_key=api_key, region=region)

    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False)
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    result = synthesizer.speak_ssml_async(ssml).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_data = result.audio_data
        return TTSResponse(
            audio_data=audio_data,
            format="riff-16khz-16bit-mono-pcm",
            voice_id=result.reason.name,
        )
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        raise RuntimeError(
            f"Azure Speech TTS SSML synthesis canceled: "
            f"{cancellation.reason} - {cancellation.error_details}"
        )
    else:
        raise RuntimeError(
            f"Azure Speech TTS SSML synthesis failed with reason: {result.reason}"
        )


def build_ssml(
    text: str,
    voice_name: str = "en-US-AriaNeural",
    rate: str = "+0%",
    pitch: str = "+0Hz",
    volume: str = "default",
) -> str:
    """Build an SSML string with voice and prosody controls for Azure Speech TTS.

    Args:
        text: The text to speak.
        voice_name: Azure neural voice name (e.g. en-US-AriaNeural).
        rate: Speech rate adjustment (e.g. "+10%", "-20%").
        pitch: Pitch adjustment (e.g. "+10Hz", "-5Hz").
        volume: Volume level (e.g. "default", "silent", "x-loud").

    Returns:
        A complete SSML document string.
    """
    ssml = (
        '<speak version="1.0" '
        'xmlns="http://www.w3.org/2001/10/synthesis" '
        'xml:lang="en-US">'
        f'<voice name="{voice_name}">'
        f'<prosody rate="{rate}" pitch="{pitch}" volume="{volume}">'
        f"{text}"
        "</prosody>"
        "</voice>"
        "</speak>"
    )
    return ssml
