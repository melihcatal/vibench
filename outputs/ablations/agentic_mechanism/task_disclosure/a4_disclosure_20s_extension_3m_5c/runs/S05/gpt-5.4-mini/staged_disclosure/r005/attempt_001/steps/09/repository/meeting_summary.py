import os
from typing import Iterable, List

from openai import OpenAI


class MeetingSummaryError(Exception):
    pass


def _build_prompt(chunks: Iterable[str]) -> str:
    parts: List[str] = [chunk.strip() for chunk in chunks if chunk and chunk.strip()]
    if not parts:
        raise MeetingSummaryError("No transcript chunks provided")
    transcript = "\n".join(parts)
    return (
        "Summarize this live meeting transcript into concise bullet points. "
        "Include decisions, action items, and open questions. Keep it brief.\n\n"
        f"Transcript:\n{transcript}"
    )


def summarize_transcript_chunks(chunks: Iterable[str], model: str = "gpt-4.1-mini") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model,
        input=_build_prompt(chunks),
    )
    return response.output_text.strip()


def summarize_transcript_chunks_stream(chunks: Iterable[str], model: str = "gpt-4.1-mini"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=model,
        input=_build_prompt(chunks),
        stream=True,
    )
    for event in response:
        if getattr(event, "type", None) == "response.output_text.delta":
            yield event.delta
