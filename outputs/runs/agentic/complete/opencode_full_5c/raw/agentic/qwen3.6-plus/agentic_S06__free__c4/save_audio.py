import os
from pathlib import Path
from typing import Optional
from speech_models import TTSResponse
from synthesize_text import synthesize_text


AUDIO_FORMAT_EXTENSIONS = {
    "audio/mpeg": ".mp3",
    "audio/opus": ".opus",
    "audio/aac": ".aac",
    "audio/flac": ".flac",
    "audio/wav": ".wav",
    "audio/pcm": ".pcm",
}


def save_audio_to_file(
    audio_bytes: bytes,
    output_path: str,
    content_type: str = "audio/mpeg",
) -> str:
    path = Path(output_path)

    if not path.suffix:
        ext = AUDIO_FORMAT_EXTENSIONS.get(content_type, ".mp3")
        path = path.with_suffix(ext)

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "wb") as f:
        f.write(audio_bytes)

    return str(path)


def save_tts_response(
    tts_response: TTSResponse,
    output_path: str,
) -> str:
    return save_audio_to_file(
        audio_bytes=tts_response.audio_bytes,
        output_path=output_path,
        content_type=tts_response.content_type,
    )


def synthesize_and_save(
    text: str,
    output_path: str,
    voice: str = "alloy",
    model: str = "tts-1",
    response_format: str = "mp3",
    speed: float = 1.0,
) -> dict:
    tts_response = synthesize_text(
        text=text,
        voice=voice,
        model=model,
        response_format=response_format,
        speed=speed,
    )

    saved_path = save_tts_response(
        tts_response=tts_response,
        output_path=output_path,
    )

    return {
        "output_path": saved_path,
        "file_size_bytes": os.path.getsize(saved_path),
        "content_type": tts_response.content_type,
        "model_used": tts_response.model_used,
        "voice_used": tts_response.voice_used,
        "duration_estimate_sec": tts_response.duration_estimate_sec,
    }
