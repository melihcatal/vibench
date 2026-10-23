import os
from typing import Optional

try:
    from openai import OpenAI
except Exception as exc:
    raise RuntimeError("openai package is required") from exc


OPENAI_TRANSCRIBE_MODEL = "gpt-4o-mini-transcribe"


def transcribe_tts_qa_sample(audio_path: str, prompt: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    with open(audio_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model=OPENAI_TRANSCRIBE_MODEL,
            file=audio_file,
            prompt=prompt,
        )
    return result.text


def transcribe_tts_qa_sample_bytes(audio_bytes: bytes, filename: str = "sample.wav", prompt: Optional[str] = None) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    from io import BytesIO

    buffer = BytesIO(audio_bytes)
    buffer.name = filename
    result = client.audio.transcriptions.create(
        model=OPENAI_TRANSCRIBE_MODEL,
        file=buffer,
        prompt=prompt,
    )
    return result.text
