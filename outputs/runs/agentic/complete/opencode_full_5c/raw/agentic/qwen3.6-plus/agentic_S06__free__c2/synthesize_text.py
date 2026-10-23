from speech_client import (
    get_openai_client,
    get_tts_model,
    validate_voice,
    validate_speed,
    validate_format,
)
from speech_models import TTSRequest, TTSResponse, normalize_tts_request


def synthesize_text(
    text: str,
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

    req = TTSRequest(
        input_text=text,
        voice=voice,
        model=model,
        response_format=response_format,
        speed=speed,
        hd=hd,
    )

    payload = normalize_tts_request(req)
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

    return TTSResponse(
        audio_bytes=audio_bytes,
        content_type=content_type_map.get(response_format, "audio/mpeg"),
        model_used=model,
        voice_used=voice,
        character_count=len(text),
    )
