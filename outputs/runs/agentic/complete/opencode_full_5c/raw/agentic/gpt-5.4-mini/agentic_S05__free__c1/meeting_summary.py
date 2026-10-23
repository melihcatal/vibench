from typing import Iterable

from openai import OpenAI


def summarize_meeting(chunks: Iterable[str]) -> str:
    client = OpenAI()
    text = "\n".join(chunks)
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Summarize this meeting transcript:\n{text}",
    )
    return response.output_text
