import os
from typing import Iterable

from openai import OpenAI

from speech_models import normalize_chunks


def summarize_meeting(chunks: Iterable[str]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = "\n".join(normalize_chunks(chunks))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Summarize this live meeting transcript:\n{text}",
    )
    return response.output_text
