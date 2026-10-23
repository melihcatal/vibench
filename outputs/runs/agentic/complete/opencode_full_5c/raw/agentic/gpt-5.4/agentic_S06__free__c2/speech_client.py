from __future__ import annotations

import os
from collections.abc import Iterable
from typing import Any

import requests

from speech_models import (
    SynthesisRequest,
    SynthesisResponse,
    VoiceOption,
    normalize_locale,
    parse_azure_voice,
)


AZURE_TTS_ENDPOINT = "https://{region}.tts.speech.microsoft.com"
AZURE_VOICES_PATH = "/cognitiveservices/voices/list"
AZURE_SYNTH_PATH = "/cognitiveservices/v1"


def get_speech_config() -> dict[str, str]:
    region = os.environ.get("AZURE_SPEECH_REGION")
    key = os.environ.get("AZURE_SPEECH_KEY")
    if not region or not key:
        raise ValueError("AZURE_SPEECH_REGION and AZURE_SPEECH_KEY are required")
    return {
        "region": region,
        "key": key,
        "endpoint": AZURE_TTS_ENDPOINT.format(region=region),
    }


def speech_headers(content_type: str = "application/ssml+xml") -> dict[str, str]:
    config = get_speech_config()
    return {
        "Ocp-Apim-Subscription-Key": config["key"],
        "Content-Type": content_type,
        "User-Agent": "azure-tts-integration",
    }


def list_voices(
    locale: str | None = None, session: requests.Session | None = None
) -> list[VoiceOption]:
    config = get_speech_config()
    client = session or requests.Session()
    response = client.get(
        f"{config['endpoint']}{AZURE_VOICES_PATH}",
        headers=speech_headers("application/json"),
        timeout=30,
    )
    response.raise_for_status()
    options = [parse_azure_voice(item) for item in response.json()]
    normalized = normalize_locale(locale) if locale else None
    if normalized:
        options = [
            item for item in options if item.locale.lower() == normalized.lower()
        ]
    return options


def choose_voice(
    locale: str,
    preferred_voice: str | None = None,
    session: requests.Session | None = None,
) -> VoiceOption:
    voices = list_voices(locale=locale, session=session)
    if preferred_voice:
        for voice in voices:
            if voice.name.lower() == preferred_voice.lower():
                return voice
    if not voices:
        raise ValueError(f"No Azure Speech voices found for locale {locale}")
    neural = [voice for voice in voices if "Neural" in voice.name]
    return neural[0] if neural else voices[0]


def build_ssml(request: SynthesisRequest) -> str:
    voice_name = request.voice or choose_voice(request.locale).name
    locale = normalize_locale(request.locale)
    escaped = (
        request.text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )
    prosody_attrs: list[str] = []
    if request.rate:
        prosody_attrs.append(f'rate="{request.rate}"')
    if request.pitch:
        prosody_attrs.append(f'pitch="{request.pitch}"')
    prosody_open = (
        f"<prosody {' '.join(prosody_attrs)}>" if prosody_attrs else "<prosody>"
    )
    if request.style:
        body = f'<mstts:express-as style="{request.style}">{prosody_open}{escaped}</prosody></mstts:express-as>'
    else:
        body = f"{prosody_open}{escaped}</prosody>"
    return (
        f'<speak version="1.0" xml:lang="{locale}" '
        f'xmlns="http://www.w3.org/2001/10/synthesis" '
        f'xmlns:mstts="https://www.w3.org/2001/mstts">'
        f'<voice name="{voice_name}">{body}</voice>'
        f"</speak>"
    )


def synthesize_ssml_payload(
    ssml: str,
    output_format: str,
    voice: str | None = None,
    locale: str | None = None,
    session: requests.Session | None = None,
) -> SynthesisResponse:
    config = get_speech_config()
    client = session or requests.Session()
    headers = speech_headers()
    headers["X-Microsoft-OutputFormat"] = output_format
    response = client.post(
        f"{config['endpoint']}{AZURE_SYNTH_PATH}",
        headers=headers,
        data=ssml.encode("utf-8"),
        timeout=60,
    )
    response.raise_for_status()
    return SynthesisResponse(
        audio_bytes=response.content,
        content_type=response.headers.get("Content-Type", "audio/mpeg"),
        voice=voice,
        locale=locale,
    )


def preferred_voice_names(voices: Iterable[VoiceOption]) -> list[str]:
    return [voice.name for voice in voices]
