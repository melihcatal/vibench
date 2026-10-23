import os
from openai import OpenAI
from typing import Optional

def transcribe_audio(audio_bytes: bytes, language: Optional[str] = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")
    client = OpenAI(api_key=api_key)
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=("speech.mp3", audio_bytes, "audio/mpeg"),
        language=language,
        response_format="text"
    )
    return str(response)
