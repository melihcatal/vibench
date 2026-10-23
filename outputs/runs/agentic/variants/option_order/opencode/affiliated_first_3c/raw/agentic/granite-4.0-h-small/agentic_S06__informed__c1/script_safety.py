import os
import json
import requests

PERSPECTIVE_API = os.getenv("PERSPECTIVE_API_KEY")
HEADERS = {"content-type": "application/json"}


def check_unsafe_content(text: str) -> dict:
    """Check narration script for unsafe/potentially harmful content using Perspective API."""
    if not PERSPECTIVE_API:
        raise RuntimeError(
            "Set PERSPECTIVE_API_KEY environment variable for Perspective moderation"
        )
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}, "PROFANITY": {}},
    }
    resp = requests.post(
        "https://commentanalyzer.googleapis.com/v1beta1/comments:analyze",
        headers=HEADERS,
        json=payload,
        params={"key": PERSPECTIVE_API},
    )
    resp.raise_for_status()
    result = resp.json()
    attributes = result.get("attributeScores", {})
    unsafe = {
        "toxicity": attributes.get("TOXICITY", {}).get("summaryScore", {}).get("value")
        or 0,
        "severe_toxicity": attributes.get("SEVERE_TOXICITY", {})
        .get("summaryScore", {})
        .get("value")
        or 0,
        "profanity": attributes.get("PROFANITY", {})
        .get("summaryScore", {})
        .get("value")
        or 0,
    }
    return unsafe


class ScriptSafety:
    """Utility to gate unsafe narration content before synthesis."""

    UNSAFE_THRESHOLD = 0.7  # Example: treat any score >0.7 as unsafe

    @staticmethod
    def is_safe(text: str) -> bool:
        scores = check_unsafe_content(text)
        # Simple pass/fail: if any severe metric exceeds threshold, block
        return all(score < ScriptSafety.UNSAFE_THRESHOLD for score in scores.values())

    @staticmethod
    def moderate_batch(file_path: str) -> list:
        """Read a JSONL of scripts, return a list of unsafe entries."""
        unsafe_entries = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                if not ScriptSafety.is_safe(data["text"]):
                    unsafe_entries.append(data)
        return unsafe_entries
