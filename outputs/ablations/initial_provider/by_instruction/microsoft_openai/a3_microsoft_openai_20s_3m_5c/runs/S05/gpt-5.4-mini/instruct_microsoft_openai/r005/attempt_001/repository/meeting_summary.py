from typing import Iterable

from openai import OpenAI

from speech_client import create_openai_client
from speech_models import normalize_transcript


def summarize_meeting(chunks: Iterable[str]) -> str:
    client: OpenAI = create_openai_client()
    transcript = "\n".join(normalize_transcript(chunk) for chunk in chunks if normalize_transcript(chunk))
    response = client.responses.create(model="gpt-4o-mini", input=f"Summarize this meeting transcript:\n{transcript}")
    return getattr(response, "output_text", "")
