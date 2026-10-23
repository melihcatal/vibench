from __future__ import annotations

from openai import OpenAI

from speech_models import MeetingSummary


class MeetingSummarizer:
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.client = OpenAI()
        self.model = model

    def summarize(self, transcript_chunks: list[str]) -> MeetingSummary:
        prompt = "\n".join(transcript_chunks)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Summarize live meeting transcript chunks with key decisions and action items."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        summary = response.choices[0].message.content or ""
        bullets = [line.lstrip("-• ") for line in summary.splitlines() if line.strip()]
        return MeetingSummary(summary=summary, bullets=bullets, raw={"provider": "openai", "model": self.model, "response_id": response.id})
