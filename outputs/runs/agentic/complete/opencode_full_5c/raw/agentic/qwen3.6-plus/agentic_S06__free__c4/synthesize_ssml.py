import httpx
from speech_client import (
    OPENAI_TTS_ENDPOINT,
    get_openai_headers,
    create_http_client,
    validate_openai_key,
    DEFAULT_TTS_MODEL,
)
from speech_models import (
    SSMLRequest,
    TTSResponse,
    estimate_duration_from_text,
)


def synthesize_ssml(
    ssml: str = "",
    text: str = "",
    voice: str = "alloy",
    model: str = DEFAULT_TTS_MODEL,
    response_format: str = "mp3",
    speed: float = 1.0,
    pitch: str = "default",
    rate: str = "medium",
    volume: str = "default",
) -> TTSResponse:
    if not validate_openai_key():
        raise ValueError("OPENAI_API_KEY is not set or invalid")

    if not ssml and text:
        ssml = SSMLRequest.build_ssml(
            text=text,
            voice_name=voice,
            pitch=pitch,
            rate=rate,
            volume=volume,
        )

    request = SSMLRequest(
        ssml=ssml,
        voice=voice,
        model=model,
        response_format=response_format,
        speed=speed,
    )

    payload = request.to_openai_payload()

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

    plain_text = ssml.replace("<speak>", "").replace("</speak>", "")
    plain_text = plain_text.replace("<voice>", "").replace("</voice>", "")
    plain_text = plain_text.replace("<prosody>", "").replace("</prosody>", "")
    duration = estimate_duration_from_text(plain_text)

    return TTSResponse(
        audio_bytes=audio_bytes,
        content_type=content_type_map.get(response_format, "audio/mpeg"),
        model_used=model,
        voice_used=voice,
        duration_estimate_sec=duration,
    )


def synthesize_ssml_to_bytes(
    ssml: str,
    voice: str = "alloy",
    model: str = DEFAULT_TTS_MODEL,
) -> bytes:
    result = synthesize_ssml(ssml=ssml, voice=voice, model=model)
    return result.audio_bytes
