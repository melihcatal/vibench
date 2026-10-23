import io
import os
from typing import Optional

from openai import OpenAI


def transcribe_tts_qa_sample(audio_path: Optional[str] = None, audio_bytes: Optional[bytes] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    if audio_bytes is not None:
        file_obj = io.BytesIO(audio_bytes)
        file_obj.name = "sample.wav"
        result = client.audio.transcriptions.create(model="whisper-1", file=file_obj)
        return result.text
    if audio_path is None:
        raise ValueError("audio_path or audio_bytes is required")
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(model="whisper-1", file=f)
    return result.text
