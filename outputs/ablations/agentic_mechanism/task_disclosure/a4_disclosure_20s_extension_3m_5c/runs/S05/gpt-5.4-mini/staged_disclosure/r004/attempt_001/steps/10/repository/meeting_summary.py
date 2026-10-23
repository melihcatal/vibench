import os
from typing import List

import openai


class MeetingSummary:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.chunks: List[str] = []

    def add_chunk(self, transcript_chunk: str) -> None:
        if transcript_chunk and transcript_chunk.strip():
            self.chunks.append(transcript_chunk.strip())

    def summarize(self) -> str:
        if not self.chunks:
            return ""
        transcript = "\n".join(self.chunks)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "Summarize live meeting transcript chunks into concise notes with decisions, action items, and open questions.",
                },
                {"role": "user", "content": transcript},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content or ""


def summarize_meeting_chunks(chunks: List[str]) -> str:
    summarizer = MeetingSummary()
    for chunk in chunks:
        summarizer.add_chunk(chunk)
    return summarizer.summarize()
