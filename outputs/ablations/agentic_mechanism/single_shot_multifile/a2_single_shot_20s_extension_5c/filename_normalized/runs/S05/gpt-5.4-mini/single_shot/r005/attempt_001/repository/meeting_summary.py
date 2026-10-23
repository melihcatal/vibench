from typing import Iterable

from openai import OpenAI
from speech_models import TranscriptEvent


class MeetingSummarizer:
    def __init__(self, api_key: str | None = None) -> None:
        self.client = OpenAI(api_key=api_key)

    def summarize(self, events: Iterable[TranscriptEvent]) -> str:
        transcript = "\n".join(event.text for event in events if event.text)
        response = self.client.responses.create(model="gpt-4.1-mini", input=f"Summarize this meeting transcript clearly and concisely:\n{transcript}")
        return response.output_text
