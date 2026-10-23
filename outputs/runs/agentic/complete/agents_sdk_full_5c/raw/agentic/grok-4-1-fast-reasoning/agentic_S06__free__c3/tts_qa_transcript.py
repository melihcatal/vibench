import os
import io
from openai import OpenAI
from typing import Optional

def transcribe_audio(
    audio_bytes: bytes,
    file_name: str = "audio.mp3",
    mime_type: str = "audio/mpeg",
    model: str = "whisper-1",
    language: Optional[str] = None
) -> str:
    """Transcribe synthesized QA samples to verify spoken output."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    audio_file = io.BytesIO(audio_bytes)
    transcript = client.audio.transcriptions.create(
        model=model,
        file=(file_name, audio_file, mime_type),
        language=language,
    )
    return transcript.text
