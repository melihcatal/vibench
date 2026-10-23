from __future__ import annotations

from speech_client import (
    create_openai_client,
    get_tts_model,
    validate_voice,
    validate_response_format,
)
from speech_models import TTSRequest, TTSResponse, normalize_text


def synthesize_text(
    text: str,
    voice: str = "alloy",
    model: str | None = None,
    response_format: str = "mp3",
    speed: float = 1.0,
    api_key: str | None = None,
) -> TTSResponse:
    normalized = normalize_text(text)
    if not normalized:
        raise ValueError("Input text is empty after normalization")

    voice = validate_voice(voice)
    response_format = validate_response_format(response_format)
    selected_model = model or get_tts_model()

    client = create_openai_client(api_key=api_key)

    request = TTSRequest(
        text=normalized,
        voice=voice,
        model=selected_model,
        response_format=response_format,
        speed=speed,
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

    tts_response = TTSResponse.from_openai_response(audio_bytes, request)
    return tts_response
