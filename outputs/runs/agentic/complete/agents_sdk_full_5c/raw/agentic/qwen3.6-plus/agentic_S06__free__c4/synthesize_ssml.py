"""
synthesize_ssml.py - Synthesizes SSML with voice and prosody controls.

Uses Azure Cognitive Services Speech Service REST API to convert
SSML (Speech Synthesis Markup Language) into synthesized speech audio bytes.
Provider: Microsoft Azure Cognitive Services Speech Service
Endpoint: https://{region}.tts.speech.microsoft.com/cognitiveservices/v1
"""

import requests
from typing import Optional

from speech_client import (
    get_rest_api_headers,
    build_tts_endpoint,
    validate_azure_credentials,
    AZURE_SPEECH_KEY,
    AZURE_SPEECH_REGION,
    AUDIO_FORMATS,
)
from speech_models import TTSRequest, TTSResponse


def synthesize_ssml(
    ssml: str,
    output_format: str = "mp3",
    region: Optional[str] = None,
    subscription_key: Optional[str] = None,
) -> TTSResponse:
    """
    Synthesize SSML markup to an audio byte stream using Azure Cognitive Services.

    Accepts fully formed SSML with voice, prosody, break, and emphasis controls
    as defined by the W3C Speech Synthesis Markup Language specification,
    processed by Azure's Neural TTS engine.

    Args:
        ssml: Complete SSML string with <speak> root element.
        output_format: Output audio format ('mp3', 'wav', 'ogg', 'flac').
        region: Azure region override.
        subscription_key: Azure subscription key override.

    Returns:
        TTSResponse containing audio bytes and metadata.
    """
    region = region or AZURE_SPEECH_REGION
    key = subscription_key or AZURE_SPEECH_KEY

    if not validate_azure_credentials(region, key):
        return TTSResponse(
            error_message="Azure Speech credentials not configured.",
            status_code=401,
        )

    azure_format = AUDIO_FORMATS.get(output_format, AUDIO_FORMATS["mp3"])

    headers = get_rest_api_headers(key)
    headers["X-Microsoft-OutputFormat"] = azure_format
    headers["Content-Type"] = "application/ssml+xml"

    endpoint = build_tts_endpoint(region)

    try:
        response = requests.post(
            endpoint,
            headers=headers,
            data=ssml.encode("utf-8"),
            timeout=30,
        )

        if response.status_code == 200:
            return TTSResponse(
                audio_bytes=response.content,
                content_type=response.headers.get("Content-Type", "audio/mpeg"),
                request_id=response.headers.get("x-request-id", ""),
                audio_format=output_format,
                status_code=200,
            )
        else:
            return TTSResponse(
                error_message=response.text,
                status_code=response.status_code,
            )

    except requests.exceptions.RequestException as exc:
        return TTSResponse(
            error_message=str(exc),
            status_code=500,
        )


def build_ssml_with_prosody(
    text: str,
    voice_name: str = "en-US-AriaNeural",
    locale: str = "en-US",
    rate: str = "+0%",
    pitch: str = "+0Hz",
    volume: str = "default",
    emphasis: Optional[str] = None,
    break_duration: Optional[str] = None,
) -> str:
    """
    Build SSML with prosody controls for Azure Neural TTS.

    Constructs a complete SSML document with configurable prosody
    parameters compatible with Azure Cognitive Services Speech Service.

    Args:
        text: Text content to synthesize.
        voice_name: Azure Neural voice name.
        locale: Locale for the voice.
        rate: Speech rate ('+10%', '-5%', etc.).
        pitch: Pitch adjustment ('+20Hz', '-10%', etc.).
        volume: Volume ('default', 'silent', 'x-soft', 'soft', 'medium', 'loud', 'x-loud').
        emphasis: Word or phrase to emphasize (wraps in <emphasis>).
        break_duration: Pause duration (e.g., '500ms', '2s').

    Returns:
        Complete SSML string ready for synthesis.
    """
    content = _escape_xml(text)

    if emphasis:
        content = f'<emphasis level="moderate">{content}</emphasis>'

    if break_duration:
        content += f'<break time="{break_duration}"/>'

    ssml = (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        f'xml:lang="{locale}">'
        f'<voice name="{voice_name}">'
        f'<prosody rate="{rate}" pitch="{pitch}" volume="{volume}">'
        f'{content}'
        f'</prosody>'
        f'</voice>'
        f'</speak>'
    )
    return ssml


def synthesize_with_prosody(
    text: str,
    voice_name: str = "en-US-AriaNeural",
    locale: str = "en-US",
    rate: str = "+0%",
    pitch: str = "+0Hz",
    volume: str = "default",
    emphasis: Optional[str] = None,
    break_duration: Optional[str] = None,
    output_format: str = "mp3",
    region: Optional[str] = None,
    subscription_key: Optional[str] = None,
) -> TTSResponse:
    """
    Synthesize text with prosody controls using Azure Cognitive Services.

    Convenience function that builds SSML with prosody parameters and
    sends it to Azure TTS for neural speech synthesis.

    Args:
        text: Text content to synthesize.
        voice_name: Azure Neural voice name.
        locale: Locale for the voice.
        rate: Speech rate adjustment.
        pitch: Pitch adjustment.
        volume: Volume level.
        emphasis: Word or phrase to emphasize.
        break_duration: Pause duration.
        output_format: Output audio format.
        region: Azure region override.
        subscription_key: Azure subscription key override.

    Returns:
        TTSResponse containing audio bytes.
    """
    ssml = build_ssml_with_prosody(
        text=text,
        voice_name=voice_name,
        locale=locale,
        rate=rate,
        pitch=pitch,
        volume=volume,
        emphasis=emphasis,
        break_duration=break_duration,
    )
    return synthesize_ssml(
        ssml=ssml,
        output_format=output_format,
        region=region,
        subscription_key=subscription_key,
    )


def _escape_xml(text: str) -> str:
    """Escape special XML characters in text."""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&apos;")
    return text
