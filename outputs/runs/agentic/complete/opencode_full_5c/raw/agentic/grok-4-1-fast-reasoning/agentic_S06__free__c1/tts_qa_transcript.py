import io
import os
from openai import OpenAI


def transcribe_audio(
    audio_bytes: bytes, model: str = "whisper-1", language: str = "en"
) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    audio_file = ("audio.mp3", io.BytesIO(audio_bytes), "audio/mpeg")
    transcript = client.audio.transcriptions.create(
        model=model,
        file=audio_file,
        language=language,
    )
    return transcript.text
