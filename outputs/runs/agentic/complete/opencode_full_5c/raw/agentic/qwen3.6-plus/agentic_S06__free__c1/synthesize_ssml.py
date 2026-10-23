from __future__ import annotations

import re

from speech_client import (
    create_openai_client,
    get_tts_model,
    validate_voice,
    validate_response_format,
)
from speech_models import (
    SSMLRequest,
    TTSResponse,
    parse_ssml_tags,
    strip_ssml_tags,
    normalize_text,
)


def synthesize_ssml(
    ssml: str,
    voice: str = "alloy",
    model: str | None = None,
    response_format: str = "mp3",
    speed: float = 1.0,
    pitch: str = "default",
    volume: str = "default",
    api_key: str | None = None,
) -> TTSResponse:
    tags = parse_ssml_tags(ssml)

    if tags:
        for tag in tags:
            if tag["tag"] == "voice":
                voice = tag["attributes"].get("name", voice)
            if tag["tag"] == "prosody":
                if "rate" in tag["attributes"]:
                    try:
                        speed = float(tag["attributes"]["rate"])
                    except ValueError:
                        pass
                if "pitch" in tag["attributes"]:
                    pitch = tag["attributes"]["pitch"]
                if "volume" in tag["attributes"]:
                    volume = tag["attributes"]["volume"]

    plain_text = strip_ssml_tags(ssml)
    normalized = normalize_text(plain_text)
    if not normalized:
        raise ValueError("SSML content is empty after stripping tags")

    voice = validate_voice(voice)
    response_format = validate_response_format(response_format)
    selected_model = model or get_tts_model()

    if speed < 0.25 or speed > 4.0:
        raise ValueError("OpenAI TTS speed must be between 0.25 and 4.0")

    client = create_openai_client(api_key=api_key)

    request = SSMLRequest(
        text=normalized,
        voice=voice,
        model=selected_model,
        response_format=response_format,
        speed=speed,
        pitch=pitch,
        volume=volume,
    )

    payload = request.to_openai_payload()

    response = client.audio.speech.create(
        model=payload["model"],
        voice=payload["voice"],
        input=payload["input"],
        response_format=payload["response_format"],
        speed=payload["speed"],
    )

    audio_bytes = response.content

    from speech_models import TTSRequest

    tts_request = TTSRequest(
        text=normalized,
        voice=voice,
        model=selected_model,
        response_format=response_format,
        speed=speed,
    )

    tts_response = TTSResponse.from_openai_response(audio_bytes, tts_request)
    return tts_response
