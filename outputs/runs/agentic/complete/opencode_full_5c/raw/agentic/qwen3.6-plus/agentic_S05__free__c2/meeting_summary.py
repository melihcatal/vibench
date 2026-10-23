import os
from dataclasses import dataclass, field
from typing import AsyncIterator, List, Optional

import openai
from openai import OpenAI

from speech_models import StreamingRecognitionResult


@dataclass
class MeetingSummary:
    chunk_summaries: List[str] = field(default_factory=list)
    full_summary: str = ""
    action_items: List[str] = field(default_factory=list)
    key_topics: List[str] = field(default_factory=list)
    transcript_length: int = 0


class MeetingSummarizer:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
        chunk_size: int = 5,
    ):
        self.model = model
        self.chunk_size = chunk_size
        self._client = OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            base_url="https://api.openai.com/v1",
        )
        self._transcript_chunks: List[str] = []
        self._chunk_summaries: List[str] = []

    def add_transcript_chunk(self, result: StreamingRecognitionResult) -> None:
        if result.is_final and result.transcript.strip():
            self._transcript_chunks.append(result.transcript)

    def summarize_chunk(self, chunk_text: str) -> str:
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a meeting summarizer. Provide a concise summary of the transcript chunk.",
                },
                {
                    "role": "user",
                    "content": f"Summarize this meeting transcript:\n\n{chunk_text}",
                },
            ],
            temperature=0.3,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()

    def generate_full_summary(self) -> MeetingSummary:
        full_transcript = " ".join(self._transcript_chunks)
        if not full_transcript.strip():
            return MeetingSummary(transcript_length=0)

        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a meeting summarizer. Provide a structured summary including: "
                        "1) A concise overall summary, 2) Key action items, 3) Main topics discussed. "
                        "Format as JSON with keys: summary, action_items, key_topics."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Analyze this meeting transcript:\n\n{full_transcript}",
                },
            ],
            temperature=0.3,
            max_tokens=500,
            response_format={"type": "json_object"},
        )
        import json

        summary_data = json.loads(response.choices[0].message.content)

        return MeetingSummary(
            chunk_summaries=self._chunk_summaries,
            full_summary=summary_data.get("summary", ""),
            action_items=summary_data.get("action_items", []),
            key_topics=summary_data.get("key_topics", []),
            transcript_length=len(self._transcript_chunks),
        )


async def summarize_meeting_live(
    caption_stream: AsyncIterator[StreamingRecognitionResult],
    api_key: Optional[str] = None,
    model: str = "gpt-4o-mini",
    summarize_interval: int = 5,
) -> AsyncIterator[MeetingSummary]:
    summarizer = MeetingSummarizer(
        api_key=api_key, model=model, chunk_size=summarize_interval
    )

    async for result in caption_stream:
        summarizer.add_transcript_chunk(result)

        if len(summarizer._transcript_chunks) >= summarizer.chunk_size:
            chunk_text = " ".join(
                summarizer._transcript_chunks[-summarizer.chunk_size :]
            )
            chunk_summary = summarizer.summarize_chunk(chunk_text)
            summarizer._chunk_summaries.append(chunk_summary)
            summarizer._transcript_chunks = summarizer._transcript_chunks[
                -summarizer.chunk_size :
            ]

            yield MeetingSummary(
                chunk_summaries=summarizer._chunk_summaries,
                transcript_length=len(summarizer._transcript_chunks),
            )
