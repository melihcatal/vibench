import os
import tempfile
from openai import OpenAI


def transcribe_audio(audio_content: bytes, language: str = "en") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
        tmp_file.write(audio_content)
        tmp_path = tmp_file.name
    try:
        with open(tmp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", file=audio_file, language=language
            )
        return transcript.text
    finally:
        os.unlink(tmp_path)
