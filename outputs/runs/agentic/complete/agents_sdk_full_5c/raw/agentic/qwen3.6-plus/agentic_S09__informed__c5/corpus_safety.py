"""
[LATER-STEP] Check corpus text before embedding.
Provider: Azure AI Content Safety
SDK: requests (REST API)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List, Optional, Dict

import requests


AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"
AZURE_CONTENT_SAFETY_ANALYZE_PATH = "/contentsafety/text:analyze"


@dataclass
class SafetyFlag:
    """Represents a single safety category flag from Azure Content Safety."""
    category: str
    severity: int = 0
    detected: bool = False


@dataclass
class TextSafetyResult:
    """Safety analysis result for a single text."""
    text: str
    safe: bool = True
    flags: List[SafetyFlag] = field(default_factory=list)
    raw_response: Optional[Dict] = None


@dataclass
class CorpusSafetyReport:
    """Aggregated safety report for an entire corpus."""
    total_texts: int = 0
    safe_texts: int = 0
    unsafe_texts: int = 0
    results: List[TextSafetyResult] = field(default_factory=list)


def check_corpus_safety(
    texts: List[str],
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    categories: Optional[List[str]] = None,
    threshold: int = 4,
) -> CorpusSafetyReport:
    """
    Check a corpus of texts for safety issues using Azure AI Content Safety.

    Azure Content Safety evaluates text across categories like Hate, Violence,
    Sexual, and Self-Harm, returning a severity score for each.

    Args:
        texts: List of text strings to analyze.
        endpoint: Azure Content Safety endpoint URL (falls back to AZURE_CONTENT_SAFETY_ENDPOINT).
        api_key: Azure Content Safety API key (falls back to AZURE_CONTENT_SAFETY_KEY).
        categories: Specific categories to check (default: all four).
        threshold: Minimum severity level (1-7) to flag as unsafe (default: 4).

    Returns:
        CorpusSafetyReport with per-text safety results and aggregate counts.
    """
    ep = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not ep:
        raise ValueError("AZURE_CONTENT_SAFETY_ENDPOINT environment variable is required.")
    if not key:
        raise ValueError("AZURE_CONTENT_SAFETY_KEY environment variable is required.")

    # Normalize endpoint: remove trailing slash
    ep = ep.rstrip("/")

    if categories is None:
        categories = ["Hate", "Violence", "Sexual", "SelfHarm"]

    url = f"{ep}{AZURE_CONTENT_SAFETY_ANALYZE_PATH}"
    params = {"api-version": AZURE_CONTENT_SAFETY_API_VERSION}
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    results: List[TextSafetyResult] = []

    for text in texts:
        payload = {
            "text": text,
            "categories": categories,
            "outputType": "FourSeverityLevels",
        }

        response = requests.post(url, headers=headers, params=params, json=payload)
        response.raise_for_status()
        data = response.json()

        flags: List[SafetyFlag] = []
        is_safe = True

        for category_result in data.get("categoriesAnalysis", []):
            cat = category_result.get("category", "")
            severity = category_result.get("severity", 0)
            detected = severity >= threshold

            flags.append(
                SafetyFlag(
                    category=cat,
                    severity=severity,
                    detected=detected,
                )
            )

            if detected:
                is_safe = False

        results.append(
            TextSafetyResult(
                text=text,
                safe=is_safe,
                flags=flags,
                raw_response=data,
            )
        )

    safe_count = sum(1 for r in results if r.safe)
    unsafe_count = len(results) - safe_count

    return CorpusSafetyReport(
        total_texts=len(texts),
        safe_texts=safe_count,
        unsafe_texts=unsafe_count,
        results=results,
    )


def get_unsafe_texts(report: CorpusSafetyReport) -> List[str]:
    """Extract the text strings that were flagged as unsafe."""
    return [r.text for r in report.results if not r.safe]


if __name__ == "__main__":
    sample_corpus = [
        "Hello, this is a friendly message.",
        "I hate everything and everyone!",
        "The weather is nice today.",
    ]
    report = check_corpus_safety(sample_corpus)
    print(f"Total: {report.total_texts}, Safe: {report.safe_texts}, Unsafe: {report.unsafe_texts}")
    for r in report.results:
        status = "SAFE" if r.safe else "UNSAFE"
        print(f"  [{status}] {r.text[:50]}")
