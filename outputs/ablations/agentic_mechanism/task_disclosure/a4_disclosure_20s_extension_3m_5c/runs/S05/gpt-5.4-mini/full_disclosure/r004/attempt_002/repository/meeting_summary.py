from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence

from openai import OpenAI


@dataclass(frozen=True)
class MeetingSummarySettings:
    model: str = "gpt-4.1-mini"
    api_key_env: str = "OPENAI_API_KEY"


def load_settings(model: Optional[str] = None) -> MeetingSummarySettings:
    return MeetingSummarySettings(model=model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))


def normalize_chunk(chunk: str) -> str:
    return " ".join(chunk.strip().split())


def build_prompt(chunks: Sequence[str]) -> str:
    cleaned: List[str] = [normalize_chunk(chunk) for chunk in chunks if normalize_chunk(chunk)]
    transcript = "\n".join(f"- {chunk}" for chunk in cleaned)
    return (
        "Summarize the following live meeting transcript chunks into concise meeting notes. "
        "Return a short summary, key decisions, action items, and open questions.\n\n"
        f"Transcript chunks:\n{transcript}"
    )


def summarize_meeting_chunks(chunks: Sequence[str], model: Optional[str] = None) -> str:
    settings = load_settings(model)
    client = OpenAI()
    response = client.responses.create(
        model=settings.model,
        input=build_prompt(chunks),
    )
    return response.output_text
