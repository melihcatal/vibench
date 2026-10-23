import os
import requests
from speech_models import (
    ModerationRequest,
    ModerationResult,
    normalize_tisane_moderation,
)


TISANE_API_URL = "https://api.tisane.ai/parse"


def moderate_transcript_text(
    text: str,
    categories: list = None,
) -> ModerationResult:
    api_key = os.environ.get("TISANE_API_KEY")
    if not api_key:
        raise ValueError("TISANE_API_KEY environment variable is required")

    if not categories:
        categories = ["violence", "sexual", "hate", "abuse", "self-harm"]

    payload = {
        "content": text,
        "settings": {
            "detect": categories,
            "language": "en",
        },
    }

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }

    response = requests.post(TISANE_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    raw_response = response.json()

    return normalize_tisane_moderation(raw_response, text)


def moderate_transcript_segments(segments: list, categories: list = None) -> list:
    results = []
    for seg in segments:
        text = seg.get("text", "") if isinstance(seg, dict) else str(seg)
        if text.strip():
            mod_result = moderate_transcript_text(text, categories)
            results.append(
                {
                    "segment": text,
                    "flagged": mod_result.flagged,
                    "categories": mod_result.categories,
                    "confidence_scores": mod_result.confidence_scores,
                }
            )
    return results


if __name__ == "__main__":
    sample_text = "This is a sample transcript segment to moderate."
    result = moderate_transcript_text(sample_text)
    print(f"Flagged: {result.flagged}")
    print(f"Categories: {result.categories}")
