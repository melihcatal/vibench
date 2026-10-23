import os
from openai import OpenAI


def transcribe_qa_sample(audio_path: str) -> str:
    client = OpenAI()
    with open(audio_path, "rb") as audio_file:
        result = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe", file=audio_file
        )
    return result.text
