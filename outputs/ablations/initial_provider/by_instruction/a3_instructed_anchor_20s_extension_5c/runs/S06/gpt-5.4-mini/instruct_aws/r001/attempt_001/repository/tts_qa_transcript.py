import os

from openai import OpenAI


def transcribe_qa_sample(audio_file, model=None):
    client = OpenAI()
    with open(audio_file, "rb") as handle:
        response = client.audio.transcriptions.create(
            model=model or os.getenv("OPENAI_TRANSCRIPTION_MODEL", "gpt-4o-mini-transcribe"),
            file=handle,
        )
    return response.text
