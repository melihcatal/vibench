import io
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def transcribe_synthesized_audio(audio_bytes: bytes, language: str = "en") -> str:
    audio_file = (io.BytesIO(audio_bytes), "speech.mp3")
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language=language,
    )
    return response.text
