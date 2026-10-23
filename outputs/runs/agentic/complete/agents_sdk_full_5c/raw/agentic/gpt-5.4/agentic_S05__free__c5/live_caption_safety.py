import os
from typing import Optional

from openai import OpenAI

from speech_models import SafetyCheckResult, normalize_transcript_text


class LiveCaptionSafety:
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def check(self, text: str) -> SafetyCheckResult:
        normalized = normalize_transcript_text(text)
        moderation = self.client.moderations.create(
            model="omni-moderation-latest",
            input=normalized,
        )
        result = moderation.results[0]
        categories = [name for name, flagged in result.categories.model_dump().items() if flagged]
        return SafetyCheckResult(
            text=normalized,
            blocked=result.flagged,
            reason=", ".join(categories) if categories else None,
        )
