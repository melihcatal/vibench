import os
from typing import Literal


class SafetyModels:
    """Local helper utilities for request/response normalization and model handling.","""

    @staticmethod
    def build_request(text: str) -> dict:
        """Prepare request payload for Anthropic moderation.",
        Anthropic expects a messages list; we send a single user message.
        """
        return {
            "model": "claude-3-5-sonnet-20240620",
            "messages": [
                {"role": "user", "content": text},
            ],
            "max_tokens": 1000,
            "temperature": 0.0,
        }

    @staticmethod
    def parse_response(resp: dict) -> dict:
        """Normalize Anthropic moderation response.",
        Anthropic returns a list of messages; for our moderation call we get a single response with content.
        Extract scores and unsafe spans.
        """
        # Anthropic moderation endpoint (via Bedrock Guardrails) returns a 'content' dict with spans
        content = resp.get("content", [])
        if not content:
            return {
                "decision": "safe",
                "scores": {},
                "unsafe_spans": [],
            }
        # Assume first element contains moderation annotations
        annotations = content[0].get("annotations", [])
        scores = {}
        unsafe_spans = []
        for ann in annotations:
            # Example structure: {"type": "moderation", "detail": {"category": "toxicity", "severity": "high"}, "offset": 5, "length": 12}
            detail = ann.get("detail", {})
            category = detail.get("category")
            severity = detail.get("severity")
            if severity == "high":
                unsafe_spans.append(
                    (ann.get("offset"), ann.get("offset") + ann.get("length", 0))
                )
            if category:
                scores[category] = 1.0  # indicator of unsafe detection
        decision = "unsafe" if unsafe_spans else "safe"
        return {
            "decision": decision,
            "scores": scores,
            "unsafe_spans": unsafe_spans,
        }

    @staticmethod
    def normalize_decision(resp: dict) -> Literal["safe", "unsafe"]:
        """Return a simple decision label.","""
        return resp.get("decision", "safe")

    @staticmethod
    def redact(text: str, unsafe_spans: list[tuple[int, int]]) -> str:
        """Redact unsafe spans with placeholder.","""
        if not unsafe_spans:
            return text
        # Sort spans descending to avoid messing up indices
        for start, end in sorted(unsafe_spans, reverse=True):
            text = text[:start] + "[REDACTED]" + text[end:]
        return text

    @staticmethod
    def threshold_check(scores: dict, thresholds: dict) -> bool:
        """Simple thresholding logic.",
        scores: dict with category scores
        thresholds: dict with category limits (0-1)
        """
        for cat, limit in thresholds.items():
            if cat in scores and scores[cat] >= limit:
                return False
        return True

    # Placeholder provider imports (replace with real SDKs when needed)
    # from safety_sdk import AnthropicClient  # import real SDK
