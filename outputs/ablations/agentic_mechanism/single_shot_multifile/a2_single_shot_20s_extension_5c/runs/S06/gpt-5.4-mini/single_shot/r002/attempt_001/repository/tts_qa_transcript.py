import os
from pathlib import Path

from openai import OpenAI


MODEL = os.environ.get('OPENAI_TRANSCRIPTION_MODEL', 'gpt-4o-mini-transcribe')


def transcribe_qa_sample(audio_path: str) -> str:
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    with Path(audio_path).open('rb') as f:
        resp = client.audio.transcriptions.create(model=MODEL, file=f)
    return resp.text
