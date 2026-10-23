import os
import tempfile
from openai import OpenAI
from typing import Optional


def transcribe_tts_audio(
    audio_bytes: bytes, language: Optional[str] = "en", model: str = "whisper-1"
) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set.")
    client = OpenAI(api_key=api_key)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
        tmp_file.write(audio_bytes)
        tmp_path = tmp_file.name
    try:
        with open(tmp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model=model, file=audio_file, language=language, response_format="text"
            )
        return str(transcript)
    finally:
        os.unlink(tmp_path)
