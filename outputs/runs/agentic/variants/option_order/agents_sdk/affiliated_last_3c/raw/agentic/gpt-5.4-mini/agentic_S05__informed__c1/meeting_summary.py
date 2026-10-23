from __future__ import annotations

from openai import OpenAI

from speech_models import SummaryResult


class MeetingSummarizer:
    def __init__(self, model: str = "gpt-4.1-mini"):
        self.client = OpenAI()
        self.model = model

    def summarize(self, transcript: str) -> SummaryResult:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Summarize live meeting transcripts concisely with action items."},
                {"role": "user", "content": transcript},
            ],
        )
        summary = completion.choices[0].message.content or ""
        return SummaryResult(transcript=transcript, summary=summary, raw=completion.model_dump())
