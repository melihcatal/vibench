import re
from speech_client import (
    get_openai_client,
    get_tts_model,
    validate_voice,
    validate_speed,
    validate_format,
)
from speech_models import SSMLRequest, TTSResponse, normalize_ssml_request


def _ssml_to_text(ssml: str) -> str:
    text = re.sub(r"<[^>]+>", " ", ssml)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def synthesize_ssml(
    ssml: str,
    voice: str = "alloy",
    model: str = None,
    response_format: str = "mp3",
    speed: float = 1.0,
    hd: bool = False,
) -> TTSResponse:
    client = get_openai_client()
    voice = validate_voice(voice)
    speed = validate_speed(speed)
    response_format = validate_format(response_format)

    if model is None:
        model = get_tts_model(hd=hd)

    req = SSMLRequest(
        ssml=ssml,
        voice=voice,
        model=model,
        response_format=response_format,
        speed=speed,
        hd=hd,
    )

    payload = normalize_ssml_request(req)
    response = client.audio.speech.create(**payload)
    audio_bytes = response.content

    content_type_map = {
        "mp3": "audio/mpeg",
        "opus": "audio/opus",
        "aac": "audio/aac",
        "flac": "audio/flac",
        "wav": "audio/wav",
        "pcm": "audio/pcm",
    }

    plain_text = _ssml_to_text(ssml)

    return TTSResponse(
        audio_bytes=audio_bytes,
        content_type=content_type_map.get(response_format, "audio/mpeg"),
        model_used=model,
        voice_used=voice,
        character_count=len(plain_text),
    )
