from typing import Iterable

from openai import OpenAI

from speech_models import TranscriptChunk, normalize_text


def summarize_meeting(chunks: Iterable[TranscriptChunk]) -> str:
    client = OpenAI()
    transcript = "\n".join(normalize_text(chunk.text) for chunk in chunks if chunk.text)
    response = client.responses.create(model="gpt-4o-mini", input=f"Summarize this meeting:\n{transcript}")
    return response.output_text
