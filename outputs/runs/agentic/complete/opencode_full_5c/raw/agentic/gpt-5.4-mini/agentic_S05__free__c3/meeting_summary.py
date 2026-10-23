from typing import Iterable

from openai import OpenAI

from speech_models import merge_partial_lines


def summarize_meeting(chunks: Iterable[str]) -> str:
    client = OpenAI()
    text = merge_partial_lines(chunks)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Summarize this meeting transcript into concise action-oriented notes: {text}",
    )
    return response.output_text
