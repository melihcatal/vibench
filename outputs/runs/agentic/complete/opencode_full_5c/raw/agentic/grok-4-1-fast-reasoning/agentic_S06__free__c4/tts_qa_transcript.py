import os
from openai import OpenAI


def transcribe_audio(audio_bytes: bytes, model: str = "whisper-1") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.audio.transcriptions.create(
        model=model, file=("qa_audio.mp3", audio_bytes, "audio/mpeg")
    )
    return response.text
