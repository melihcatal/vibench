from __future__ import annotations

import os
from typing import Any, Dict, List

from openai import OpenAI


class LiveCaptionSafetyChecker:
    def __init__(self, model: str = "omni-moderation-latest") -> None:
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def check_text(self, transcript_text: str) -> Dict[str, Any]:
        response = self.client.moderations.create(
            model=self.model,
            input=transcript_text,
        )
        result = response.results[0]
        return {
            "flagged": result.flagged,
            "categories": result.categories.model_dump(),
            "category_scores": result.category_scores.model_dump(),
        }

    def check_batch(self, transcript_lines: List[str]) -> List[Dict[str, Any]]:
        return [self.check_text(line) for line in transcript_lines]
