from __future__ import annotations

from openai import OpenAI

from speech_models import TextToSpeechResponse

DEFAULT_TRANSCRIBE_MODEL = "gpt-4o-mini-transcribe"


def transcribe_qa_sample(sample: TextToSpeechResponse) -> str:
    client = OpenAI()
    response = client.audio.transcriptions.create(model=DEFAULT_TRANSCRIBE_MODEL, file=("sample.mp3", sample.audio_bytes, sample.content_type))
    return response.text
