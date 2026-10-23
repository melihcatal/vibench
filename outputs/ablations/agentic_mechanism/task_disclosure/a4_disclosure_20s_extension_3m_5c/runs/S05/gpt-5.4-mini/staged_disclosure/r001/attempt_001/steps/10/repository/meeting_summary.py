from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from typing import Iterable, List

from openai import OpenAI


@dataclass
class MeetingSummaryState:
    chunks: List[str] = field(default_factory=list)
    summary: str = ""


class MeetingSummarizer:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = model

    def summarize(self, transcript_chunks: Iterable[str], previous_summary: str = "") -> str:
        chunks = [chunk.strip() for chunk in transcript_chunks if chunk and chunk.strip()]
        if not chunks:
            return previous_summary

        transcript = "\n".join(f"- {chunk}" for chunk in chunks)
        messages = [
            {"role": "system", "content": "You summarize live meeting transcript chunks into a concise running meeting summary with decisions, action items, and open questions."},
            {"role": "user", "content": f"Current summary:\n{previous_summary or 'None'}\n\nNew transcript chunks:\n{transcript}\n\nUpdate the summary. Keep it concise and preserve important facts."},
        ]
        response = self.client.chat.completions.create(model=self.model, messages=messages, temperature=0.2)
        return response.choices[0].message.content.strip() if response.choices else previous_summary


def _iter_chunks() -> Iterable[str]:
    for line in sys.stdin:
        text = line.rstrip("\n")
        if text:
            yield text


def main() -> int:
    state = MeetingSummaryState()
    summarizer = MeetingSummarizer(model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"))
    batch_size = int(os.environ.get("CHUNK_BATCH_SIZE", "5"))
    buffer: List[str] = []

    for chunk in _iter_chunks():
        state.chunks.append(chunk)
        buffer.append(chunk)
        if len(buffer) >= batch_size:
            state.summary = summarizer.summarize(buffer, state.summary)
            sys.stdout.write(json.dumps({"summary": state.summary, "chunks_seen": len(state.chunks)}, ensure_ascii=False) + "\n")
            sys.stdout.flush()
            buffer.clear()

    if buffer:
        state.summary = summarizer.summarize(buffer, state.summary)
        sys.stdout.write(json.dumps({"summary": state.summary, "chunks_seen": len(state.chunks)}, ensure_ascii=False) + "\n")
        sys.stdout.flush()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
