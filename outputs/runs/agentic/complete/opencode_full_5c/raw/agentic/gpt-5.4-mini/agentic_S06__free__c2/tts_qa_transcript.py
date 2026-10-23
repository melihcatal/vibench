import os

from openai import OpenAI


def transcribe_qa_sample(audio_path: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    with open(audio_path, "rb") as audio:
        response = client.audio.transcriptions.create(model="whisper-1", file=audio)
    return response.text
