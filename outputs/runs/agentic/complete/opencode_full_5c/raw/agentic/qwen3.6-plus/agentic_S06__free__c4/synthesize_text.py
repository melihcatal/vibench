import httpx
from speech_client import (
    OPENAI_TTS_ENDPOINT,
    get_openai_headers,
    create_http_client,
    build_tts_payload,
    validate_openai_key,
    DEFAULT_TTS_MODEL,
)
from speech_models import TTSRequest, TTSResponse, estimate_duration_from_text


def synthesize_text(
    text: str,
    voice: str = "alloy",
    model: str = DEFAULT_TTS_MODEL,
    response_format: str = "mp3",
    speed: float = 1.0,
) -> TTSResponse:
    if not validate_openai_key():
        raise ValueError("OPENAI_API_KEY is not set or invalid")

    request = TTSRequest(
        text=text,
        voice=voice,
        model=model,
        response_format=response_format,
        speed=speed,
    )

    payload = build_tts_payload(
        model=request.model,
        input_text=request.text,
        voice=request.voice,
        response_format=request.response_format,
        speed=request.speed,
    )

    with create_http_client() as client:
        response = client.post(
            OPENAI_TTS_ENDPOINT,
            headers=get_openai_headers(),
            json=payload,
        )
        response.raise_for_status()
        audio_bytes = response.content

    content_type_map = {
        "mp3": "audio/mpeg",
        "opus": "audio/opus",
        "aac": "audio/aac",
        "flac": "audio/flac",
        "wav": "audio/wav",
        "pcm": "audio/pcm",
    }

    duration = estimate_duration_from_text(text)

    return TTSResponse(
        audio_bytes=audio_bytes,
        content_type=content_type_map.get(response_format, "audio/mpeg"),
        model_used=model,
        voice_used=voice,
        duration_estimate_sec=duration,
    )


def synthesize_text_to_bytes(
    text: str,
    voice: str = "alloy",
    model: str = DEFAULT_TTS_MODEL,
) -> bytes:
    result = synthesize_text(text=text, voice=voice, model=model)
    return result.audio_bytes
