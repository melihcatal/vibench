import os
from dataclasses import dataclass, field
from typing import AsyncIterator, Dict, List, Optional, Tuple

import openai
from openai import OpenAI

from speech_models import StreamingRecognitionResult


@dataclass
class SafetyCheckResult:
    text: str
    is_unsafe: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    scores: Dict[str, float] = field(default_factory=dict)
    flagged_categories: List[str] = field(default_factory=list)


class LiveCaptionSafetyChecker:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "omni-moderation-latest",
        threshold: float = 0.5,
    ):
        self.model = model
        self.threshold = threshold
        self._client = OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            base_url="https://api.openai.com/v1",
        )

    def check_text(self, text: str) -> SafetyCheckResult:
        if not text.strip():
            return SafetyCheckResult(text=text, is_unsafe=False)

        moderation = self._client.moderations.create(
            model=self.model,
            input=text,
        )

        result = moderation.results[0]
        categories = {
            cat: getattr(result.categories, cat)
            for cat in result.categories.model_dump()
        }
        scores = {
            cat: getattr(result.category_scores, cat)
            for cat in result.category_scores.model_dump()
        }
        flagged = [cat for cat, flagged in categories.items() if flagged]

        return SafetyCheckResult(
            text=text,
            is_unsafe=result.flagged,
            categories=categories,
            scores=scores,
            flagged_categories=flagged,
        )

    def check_result(
        self, result: StreamingRecognitionResult
    ) -> Tuple[StreamingRecognitionResult, SafetyCheckResult]:
        safety = self.check_text(result.transcript)
        return result, safety


async def check_live_caption_safety(
    caption_stream: AsyncIterator[StreamingRecognitionResult],
    api_key: Optional[str] = None,
    model: str = "omni-moderation-latest",
    threshold: float = 0.5,
) -> AsyncIterator[Tuple[StreamingRecognitionResult, SafetyCheckResult]]:
    checker = LiveCaptionSafetyChecker(
        api_key=api_key, model=model, threshold=threshold
    )

    async for result in caption_stream:
        yield checker.check_result(result)


async def filter_unsafe_captions(
    caption_stream: AsyncIterator[StreamingRecognitionResult],
    api_key: Optional[str] = None,
) -> AsyncIterator[StreamingRecognitionResult]:
    checker = LiveCaptionSafetyChecker(api_key=api_key)

    async for result in caption_stream:
        _, safety = checker.check_result(result)
        if not safety.is_unsafe:
            yield result
