import os
from pathlib import Path
from speech_models import TTSResponse


def save_audio(
    tts_response: TTSResponse, output_path: str = None, overwrite: bool = False
) -> str:
    if output_path is None:
        ext = "mp3" if "mp3" in tts_response.format else "wav"
        output_path = f"tts_output_{tts_response.voice_id}.{ext}"

    path = Path(output_path)

    if path.exists() and not overwrite:
        base = path.stem
        suffix = path.suffix
        counter = 1
        while path.exists():
            output_path = f"{base}_{counter}{suffix}"
            path = Path(output_path)
            counter += 1

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "wb") as f:
        f.write(tts_response.audio_data)

    return str(path)
