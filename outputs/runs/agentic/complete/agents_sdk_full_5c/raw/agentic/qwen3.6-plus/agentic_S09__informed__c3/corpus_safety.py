"""
corpus_safety.py - Check corpus text before embedding.

Provider: Google Perspective API
Interface: REST via requests
Auth: PERSPECTIVE_API_KEY
"""

import os
from dataclasses import dataclass, field
from typing import Any

import requests


PERSPECTIVE_API_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)

_api_key = os.environ.get("PERSPECTIVE_API_KEY", "")


@dataclass
class SafetyScore:
    """A single attribute score from Perspective API."""

    attribute: str
    score: float
    flagged: bool = False


@dataclass
class CorpusSafetyResult:
    """Aggregated safety assessment for a piece of text."""

    text_preview: str
    scores: list[SafetyScore] = field(default_factory=list)
    overall_safe: bool = True
    threshold: float = 0.7

    def flag_summary(self) -> list[str]:
        return [s.attribute for s in self.scores if s.flagged]


def analyze_text_perspective(
    text: str,
    threshold: float = 0.7,
    attributes: list[str] | None = None,
) -> CorpusSafetyResult:
    """Check text safety attributes using Google Perspective API.

    Sends the text to the Perspective API for toxicity and safety analysis.
    Attributes scored include TOXICITY, SEVERE_TOXICITY, INSULT, and PROFANITY.

    Args:
        text: The input text to evaluate.
        threshold: Score above which an attribute is flagged (default 0.7).
        attributes: List of Perspective API attributes to evaluate.

    Returns:
        CorpusSafetyResult with per-attribute scores and flags.
    """
    if not _api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required.")

    if attributes is None:
        attributes = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "INSULT",
            "PROFANITY",
            "THREAT",
        ]

    payload: dict[str, Any] = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
        "languages": ["en"],
    }

    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": _api_key},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    result = CorpusSafetyResult(
        text_preview=text[:100],
        threshold=threshold,
    )

    attribute_scores = data.get("attributeScores", {})
    for attr_name, attr_data in attribute_scores.items():
        summary = attr_data.get("summaryScore", {})
        score = summary.get("value", 0.0)
        flagged = score >= threshold
        result.scores.append(
            SafetyScore(attribute=attr_name, score=score, flagged=flagged)
        )
        if flagged:
            result.overall_safe = False

    return result


def check_corpus_before_embedding(
    texts: list[str],
    threshold: float = 0.7,
) -> list[CorpusSafetyResult]:
    """Run safety checks on a corpus of texts before sending to an embeddings API.

    Uses the Perspective API to screen each text for harmful content.

    Args:
        texts: List of texts to check.
        threshold: Flagging threshold for each attribute score.

    Returns:
        List of CorpusSafetyResult, one per input text.
    """
    results: list[CorpusSafetyResult] = []
    for text in texts:
        if not text.strip():
            results.append(
                CorpusSafetyResult(text_preview="", overall_safe=True)
            )
            continue
        safety = analyze_text_perspective(text, threshold=threshold)
        results.append(safety)
    return results


def main() -> None:
    sample_texts = [
        "Welcome to our community guidelines discussion.",
        "This is a very rude and offensive message that contains bad words.",
        "Machine learning models require careful evaluation.",
    ]
    results = check_corpus_before_embedding(sample_texts)
    for text, safety in zip(sample_texts, results):
        status = "SAFE" if safety.overall_safe else "FLAGGED"
        flags = safety.flag_summary()
        print(f"[{status}] {text[:60]}...")
        if flags:
            print(f"  Flags: {', '.join(flags)}")
        print()


if __name__ == "__main__":
    main()
