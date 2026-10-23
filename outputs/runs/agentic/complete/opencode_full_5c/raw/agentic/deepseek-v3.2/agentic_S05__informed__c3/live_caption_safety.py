import os
import asyncio
from typing import AsyncGenerator, Dict, Any, Optional
import requests
import json


class LiveCaptionSafetyChecker:
    def __init__(self):
        self.api_key = os.environ.get("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

        self.api_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

        self.attributes = {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
        }

    async def check_text_safety(
        self, text: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if not text.strip():
            return {
                "text": text,
                "is_safe": True,
                "scores": {},
                "flags": [],
                "overall_risk": "LOW",
            }

        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": self.attributes,
            "doNotStore": True,
        }

        if context:
            payload["context"] = context

        try:
            params = {"key": self.api_key}
            response = requests.post(self.api_url, params=params, json=payload)
            response.raise_for_status()

            result = response.json()

            scores = {}
            flags = []

            for attr_name, attr_data in result.get("attributeScores", {}).items():
                score = attr_data.get("summaryScore", {}).get("value", 0.0)
                scores[attr_name] = score

                if score > 0.7:
                    flags.append(attr_name)

            overall_risk = "HIGH" if len(flags) > 0 else "LOW"
            if 0.3 < max(scores.values(), default=0.0) <= 0.7:
                overall_risk = "MEDIUM"

            return {
                "text": text,
                "is_safe": overall_risk == "LOW",
                "scores": scores,
                "flags": flags,
                "overall_risk": overall_risk,
                "provider": "Perspective API",
            }

        except Exception as e:
            return {
                "text": text,
                "is_safe": True,
                "scores": {},
                "flags": [],
                "overall_risk": "UNKNOWN",
                "error": str(e),
                "provider": "Perspective API",
            }

    async def stream_safety_check(
        self, caption_stream: AsyncGenerator[Dict[str, Any], None]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        async for caption in caption_stream:
            caption_text = caption.get("text", "")
            is_final = caption.get("is_final", True)

            safety_result = await self.check_text_safety(caption_text)

            result = {
                **caption,
                "safety_check": safety_result,
                "is_safe": safety_result["is_safe"],
                "safety_scores": safety_result["scores"],
                "safety_flags": safety_result["flags"],
                "safety_metadata": {
                    "overall_risk": safety_result["overall_risk"],
                    "provider": "Perspective API",
                },
            }

            yield result

    def set_custom_attributes(self, attributes: Dict[str, Dict]):
        self.attributes = attributes

    def get_attribute_thresholds(self) -> Dict[str, float]:
        return {
            "TOXICITY": 0.7,
            "SEVERE_TOXICITY": 0.7,
            "IDENTITY_ATTACK": 0.7,
            "INSULT": 0.7,
            "PROFANITY": 0.7,
            "THREAT": 0.7,
            "SEXUALLY_EXPLICIT": 0.7,
            "FLIRTATION": 0.7,
        }


class SafetyFilter:
    def __init__(self, safety_checker: LiveCaptionSafetyChecker):
        self.safety_checker = safety_checker
        self.unsafe_count = 0
        self.total_checked = 0

    async def filter_unsafe_captions(
        self, caption_stream: AsyncGenerator[Dict[str, Any], None]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        async for caption in caption_stream:
            self.total_checked += 1

            caption_text = caption.get("text", "")
            safety_result = await self.safety_checker.check_text_safety(caption_text)

            if safety_result["is_safe"]:
                yield {**caption, "safety_result": safety_result, "filtered": False}
            else:
                self.unsafe_count += 1
                yield {
                    **caption,
                    "safety_result": safety_result,
                    "filtered": True,
                    "filtered_text": "[CONTENT FILTERED]",
                    "filter_reason": safety_result["flags"],
                }

    def get_stats(self) -> Dict[str, Any]:
        if self.total_checked == 0:
            return {"total_checked": 0, "unsafe_count": 0, "unsafe_percentage": 0.0}

        return {
            "total_checked": self.total_checked,
            "unsafe_count": self.unsafe_count,
            "unsafe_percentage": (self.unsafe_count / self.total_checked) * 100,
        }


async def check_live_caption_safety(
    caption_stream: AsyncGenerator[Dict[str, Any], None], filter_unsafe: bool = False
) -> AsyncGenerator[Dict[str, Any], None]:
    safety_checker = LiveCaptionSafetyChecker()

    if filter_unsafe:
        safety_filter = SafetyFilter(safety_checker)
        async for filtered in safety_filter.filter_unsafe_captions(caption_stream):
            yield filtered
    else:
        async for checked in safety_checker.stream_safety_check(caption_stream):
            yield checked


class BatchSafetyChecker:
    def __init__(self):
        self.api_key = os.environ.get("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

        self.api_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    async def batch_check(self, texts: list, batch_size: int = 10) -> list:
        results = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            batch_results = await asyncio.gather(
                *[self._check_single(text) for text in batch], return_exceptions=True
            )

            for j, result in enumerate(batch_results):
                if isinstance(result, Exception):
                    results.append(
                        {
                            "text": batch[j] if j < len(batch) else "",
                            "is_safe": True,
                            "scores": {},
                            "flags": [],
                            "overall_risk": "UNKNOWN",
                            "error": str(result),
                        }
                    )
                else:
                    results.append(result)

            await asyncio.sleep(0.1)

        return results

    async def _check_single(self, text: str) -> Dict[str, Any]:
        safety_checker = LiveCaptionSafetyChecker()
        return await safety_checker.check_text_safety(text)


async def monitor_safety_trends(
    caption_stream: AsyncGenerator[Dict[str, Any], None], window_size: int = 50
) -> AsyncGenerator[Dict[str, Any], None]:
    safety_checker = LiveCaptionSafetyChecker()
    recent_scores = []

    async for caption in caption_stream:
        caption_text = caption.get("text", "")
        safety_result = await safety_checker.check_text_safety(caption_text)

        recent_scores.append(max(safety_result["scores"].values(), default=0.0))
        if len(recent_scores) > window_size:
            recent_scores.pop(0)

        avg_score = sum(recent_scores) / len(recent_scores) if recent_scores else 0.0
        max_recent = max(recent_scores) if recent_scores else 0.0

        trend = "STABLE"
        if len(recent_scores) >= 10:
            recent_avg = sum(recent_scores[-10:]) / 10
            older_avg = (
                sum(recent_scores[:-10]) / (len(recent_scores) - 10)
                if len(recent_scores) > 10
                else recent_avg
            )
            if recent_avg > older_avg * 1.5:
                trend = "INCREASING"
            elif recent_avg < older_avg * 0.5:
                trend = "DECREASING"

        yield {
            **caption,
            "safety_result": safety_result,
            "trend_analysis": {
                "average_risk_score": avg_score,
                "max_recent_risk": max_recent,
                "trend": trend,
                "window_size": len(recent_scores),
            },
        }


if __name__ == "__main__":

    async def mock_caption_stream():
        captions = [
            {"text": "Hello everyone, welcome to the meeting", "is_final": True},
            {"text": "This is a friendly discussion", "is_final": True},
            {"text": "I think that's a terrible idea", "is_final": False},
            {"text": "Let's work together constructively", "is_final": True},
        ]

        for caption in captions:
            yield caption
            await asyncio.sleep(0.5)

    async def main():
        safety_checker = LiveCaptionSafetyChecker()

        async for checked in safety_checker.stream_safety_check(mock_caption_stream()):
            print(f"Caption: {checked.get('text')}")
            print(f"Safe: {checked.get('is_safe')}")
            print(f"Risk: {checked.get('safety_metadata', {}).get('overall_risk')}")
            print(f"Flags: {checked.get('safety_flags', [])}")
            print("---")

    asyncio.run(main())
