import os
import requests
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class SafetyResult:
    """Result of content safety analysis."""

    text: str
    is_safe: bool
    categories: Dict[str, float]
    severity_scores: Dict[str, float]
    flagged_categories: List[str]
    confidence: float


class LiveCaptionSafetyChecker:
    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None):
        self.api_key = api_key or os.getenv("AZURE_CONTENT_SAFETY_KEY")
        self.endpoint = endpoint or os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")

        if not self.api_key or not self.endpoint:
            raise ValueError(
                "Azure Content Safety credentials not found. "
                "Set AZURE_CONTENT_SAFETY_KEY and AZURE_CONTENT_SAFETY_ENDPOINT environment variables."
            )

        self.base_url = f"{self.endpoint.rstrip('/')}/contentsafety/text:analyze"
        self.api_version = "2023-10-01"

    def check_text(
        self, text: str, categories: Optional[List[str]] = None
    ) -> SafetyResult:
        """Check text for unsafe content using Azure AI Content Safety."""
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json",
        }

        params = {"api-version": self.api_version}

        request_body = {
            "text": text,
            "categories": categories or ["Hate", "SelfHarm", "Sexual", "Violence"],
        }

        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                params=params,
                json=request_body,
                timeout=10,
            )
            response.raise_for_status()

            result_data = response.json()

            return self._parse_safety_result(text, result_data)

        except requests.exceptions.RequestException as e:
            print(f"Error calling Azure Content Safety API: {e}")
            return SafetyResult(
                text=text,
                is_safe=True,  # Default to safe on error
                categories={},
                severity_scores={},
                flagged_categories=[],
                confidence=0.0,
            )

    def _parse_safety_result(
        self, text: str, result_data: Dict[str, Any]
    ) -> SafetyResult:
        """Parse Azure Content Safety API response."""
        categories_analysis = result_data.get("categoriesAnalysis", [])

        categories = {}
        severity_scores = {}
        flagged_categories = []

        for category_analysis in categories_analysis:
            category = category_analysis.get("category", "")
            severity = category_analysis.get("severity", 0)

            categories[category] = severity
            severity_scores[category] = severity

            if severity > 0:
                flagged_categories.append(category)

        is_safe = len(flagged_categories) == 0

        confidence = (
            1.0 - (sum(severity_scores.values()) / (len(severity_scores) * 7.0))
            if severity_scores
            else 1.0
        )

        return SafetyResult(
            text=text,
            is_safe=is_safe,
            categories=categories,
            severity_scores=severity_scores,
            flagged_categories=flagged_categories,
            confidence=confidence,
        )

    def check_caption(self, caption: Dict[str, Any]) -> Dict[str, Any]:
        """Check a caption dictionary for safety."""
        caption_text = caption.get("text", "")

        safety_result = self.check_text(caption_text)

        return {
            "caption": caption,
            "safety_result": safety_result,
            "should_block": not safety_result.is_safe,
            "flagged_reasons": safety_result.flagged_categories,
        }

    def check_captions_batch(
        self, captions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Check multiple captions for safety."""
        results = []

        for caption in captions:
            results.append(self.check_caption(caption))

        return results


class RealTimeSafetyMonitor:
    def __init__(self, safety_checker: LiveCaptionSafetyChecker):
        self.safety_checker = safety_checker
        self.flagged_count = 0
        self.total_checked = 0

    async def monitor_stream(self, caption_stream):
        """Monitor a stream of captions for safety."""
        async for caption in caption_stream:
            self.total_checked += 1

            if caption.get("is_final", False):
                caption_text = caption.get("text", "")

                if caption_text.strip():
                    safety_check = self.safety_checker.check_caption(caption)

                    if safety_check["should_block"]:
                        self.flagged_count += 1
                        print(f"⚠️  Unsafe caption detected: {caption_text}")
                        print(
                            f"   Flagged categories: {safety_check['flagged_reasons']}"
                        )

                    yield {
                        "caption": caption,
                        "safety_check": safety_check,
                        "stats": {
                            "flagged_count": self.flagged_count,
                            "total_checked": self.total_checked,
                            "flag_rate": self.flagged_count / self.total_checked
                            if self.total_checked > 0
                            else 0,
                        },
                    }

    def get_stats(self) -> Dict[str, Any]:
        """Get monitoring statistics."""
        return {
            "flagged_count": self.flagged_count,
            "total_checked": self.total_checked,
            "flag_rate": self.flagged_count / self.total_checked
            if self.total_checked > 0
            else 0,
        }


def create_safety_filter(safety_checker: LiveCaptionSafetyChecker):
    """Create a filter function for unsafe captions."""

    def filter_unsafe_captions(caption_stream):
        async for caption in caption_stream:
            if caption.get("is_final", False):
                caption_text = caption.get("text", "")

                if caption_text.strip():
                    safety_result = safety_checker.check_text(caption_text)

                    if safety_result.is_safe:
                        yield caption
                    else:
                        print(f"Filtered unsafe caption: {caption_text}")
                        print(f"Flagged categories: {safety_result.flagged_categories}")
                else:
                    yield caption
            else:
                yield caption

    return filter_unsafe_captions


if __name__ == "__main__":
    checker = LiveCaptionSafetyChecker()

    test_texts = [
        "Hello everyone, welcome to the meeting.",
        "This is a hateful and violent statement that should be flagged.",
        "Let's discuss the project timeline and deliverables.",
    ]

    for text in test_texts:
        result = checker.check_text(text)
        print(f"Text: {text[:50]}...")
        print(f"Safe: {result.is_safe}")
        print(f"Flagged categories: {result.flagged_categories}")
        print(f"Severity scores: {result.severity_scores}")
        print()
