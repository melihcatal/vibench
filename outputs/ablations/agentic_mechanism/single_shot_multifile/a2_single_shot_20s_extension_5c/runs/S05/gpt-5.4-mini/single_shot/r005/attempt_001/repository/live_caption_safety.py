from typing import Iterable, List

from speech_models import TranscriptEvent
from openai import OpenAI


class CaptionSafetyChecker:
    def __init__(self, api_key: str | None = None) -> None:
        self.client = OpenAI(api_key=api_key)

    def check(self, events: Iterable[TranscriptEvent]) -> List[dict]:
        results = []
        for event in events:
            moderation = self.client.moderations.create(model="omni-moderation-latest", input=event.text)
            flagged = bool(moderation.results[0].flagged)
            results.append({"text": event.text, "flagged": flagged, "categories": moderation.results[0].categories.model_dump()})
        return results
