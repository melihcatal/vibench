from __future__ import annotations

from typing import Iterable, Optional

from openai import OpenAI

from speech_models import SummaryRequest, join_transcript_chunks

SUMMARY_MODEL = "gpt-4.1-mini"


class MeetingSummarizer:
    def __init__(self, api_key: Optional[str] = None) -> None:
        import os

        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def summarize(self, chunks: Iterable[str], request: SummaryRequest) -> str:
        transcript = join_transcript_chunks(chunks)
        system = "You summarize meeting transcripts into concise notes."
        if request.bullets:
            instruction = "Return bullet points, action items, and key decisions."
        else:
            instruction = "Return a concise paragraph summary."
        if request.meeting_topic:
            instruction = f"Topic: {request.meeting_topic}. {instruction}"
        response = self.client.chat.completions.create(
            model=SUMMARY_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": f"Transcript:\n{transcript}\n\n{instruction}"},
            ],
        )
        return response.choices[0].message.content or ""


def summarize_live_meeting(chunks: Iterable[str], meeting_topic: Optional[str] = None) -> str:
    return MeetingSummarizer().summarize(chunks, SummaryRequest(meeting_topic=meeting_topic))
