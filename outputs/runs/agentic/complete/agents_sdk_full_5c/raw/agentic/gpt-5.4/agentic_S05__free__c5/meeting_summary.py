import os
from typing import Iterable, Optional

from openai import OpenAI

from speech_models import SummaryResult, merge_caption_text

SUMMARY_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


class MeetingSummarizer:
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def summarize(self, transcript_chunks: Iterable[str]) -> SummaryResult:
        chunks = [chunk for chunk in transcript_chunks if chunk.strip()]
        merged = merge_caption_text([])
        merged = " ".join(chunk.strip() for chunk in chunks)
        response = self.client.responses.create(
            model=SUMMARY_MODEL,
            input=[
                {"role": "system", "content": "Summarize this live meeting transcript into concise action items and key decisions."},
                {"role": "user", "content": merged},
            ],
        )
        return SummaryResult(
            summary=response.output_text.strip(),
            source_chunk_count=len(chunks),
        )
