from typing import List

from openai import OpenAI

from speech_models import normalize_text


class LiveCaptionSafetyChecker:
    def __init__(self) -> None:
        self._client = OpenAI()

    def check(self, caption_text: str) -> List[str]:
        text = normalize_text(caption_text)
        if not text:
            return []
        response = self._client.moderations.create(
            model="omni-moderation-latest",
            input=text,
        )
        results = []
        for item in response.results:
            if item.flagged:
                results.append("flagged")
        return results

