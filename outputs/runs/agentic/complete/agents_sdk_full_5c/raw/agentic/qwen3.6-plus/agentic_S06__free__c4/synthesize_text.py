"""
synthesize_text.py - Synthesizes plain text to an audio byte stream.

Uses Azure Cognitive Services Speech Service REST API to convert
plain text into synthesized speech audio bytes.
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


def synthesize_text(
    text: str,
    voice_name: str = "en-US-AriaNeural",
    locale: str = "en-US",
    output_format: str = "mp3",
    region: Optional[str] = None,
    subscription_key: Optional[str] = None,
) -> TTSResponse:
    """
    Synthesize plain text to an audio byte stream using Azure Cognitive Services.

    Sends a POST request to the Azure TTS REST API endpoint with SSML
    generated from the plain text input.

    Args:
        text: Plain text to synthesize.
        voice_name: Azure Neural voice name (e.g., 'en-US-AriaNeural').
        locale: Locale string for the voice.
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

    request = TTSRequest(
        text=text,
        voice_name=voice_name,
        locale=locale,
        output_format=azure_format,
    )

    ssml_payload = request.to_rest_payload()

    headers = get_rest_api_headers(key)
    headers["X-Microsoft-OutputFormat"] = azure_format
    headers["Content-Type"] = "application/ssml+xml"

    endpoint = build_tts_endpoint(region)

    try:
        response = requests.post(
            endpoint,
            headers=headers,
            data=ssml_payload.encode("utf-8"),
            timeout=30,
        )

        if response.status_code == 200:
            return TTSResponse(
                audio_bytes=response.content,
                content_type=response.headers.get("Content-Type", "audio/mpeg"),
                request_id=response.headers.get("x-request-id", ""),
                voice_name=voice_name,
                audio_format=output_format,
                status_code=200,
            )
        else:
            return TTSResponse(
                error_message=response.text,
                status_code=response.status_code,
                voice_name=voice_name,
            )

    except requests.exceptions.RequestException as exc:
        return TTSResponse(
            error_message=str(exc),
            status_code=500,
            voice_name=voice_name,
        )


def synthesize_text_stream(
    text: str,
    voice_name: str = "en-US-JennyNeural",
    locale: str = "en-US",
    output_format: str = "mp3",
    region: Optional[str] = None,
    subscription_key: Optional[str] = None,
    chunk_size: int = 4096,
):
    """
    Synthesize plain text and stream the audio bytes in chunks.

    Uses Azure Cognitive Services Speech Service and yields audio
    data in configurable chunk sizes for memory-efficient processing.

    Args:
        text: Plain text to synthesize.
        voice_name: Azure Neural voice name.
        locale: Locale string.
        output_format: Output audio format.
        region: Azure region override.
        subscription_key: Azure subscription key override.
        chunk_size: Size of each yielded chunk in bytes.

    Yields:
        Bytes chunks of synthesized audio.
    """
    region = region or AZURE_SPEECH_REGION
    key = subscription_key or AZURE_SPEECH_KEY

    if not validate_azure_credentials(region, key):
        raise ValueError("Azure Speech credentials not configured.")

    azure_format = AUDIO_FORMATS.get(output_format, AUDIO_FORMATS["mp3"])

    request = TTSRequest(
        text=text,
        voice_name=voice_name,
        locale=locale,
        output_format=azure_format,
    )

    ssml_payload = request.to_rest_payload()

    headers = get_rest_api_headers(key)
    headers["X-Microsoft-OutputFormat"] = azure_format
    headers["Content-Type"] = "application/ssml+xml"

    endpoint = build_tts_endpoint(region)

    response = requests.post(
        endpoint,
        headers=headers,
        data=ssml_payload.encode("utf-8"),
        timeout=60,
        stream=True,
    )

    response.raise_for_status()

    for chunk in response.iter_content(chunk_size=chunk_size):
        if chunk:
            yield chunk
