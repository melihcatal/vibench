"""
visual_safety_text.py - Check generated visual labels for unsafe text
using Google Perspective API for text content safety.
"""

import json
import os
import sys
from typing import Dict, Any, List, Optional

import requests

from vision_models import DetectedLabel, DetectedTextRegion


PERSPECTIVE_API_KEY_ENV = "PERSPECTIVE_API_KEY"
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def get_perspective_api_key() -> str:
    key = os.environ.get(PERSPECTIVE_API_KEY_ENV)
    if not key:
        raise RuntimeError(f"Missing environment variable: {PERSPECTIVE_API_KEY_ENV}")
    return key


def check_text_safety(
    text: str,
    *,
    api_key: Optional[str] = None,
    attributes: Optional[List[str]] = None,
    languages: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Check text for unsafe content using Google Perspective API.

    Provider: Perspective API (requests REST)
    Auth: PERSPECTIVE_API_KEY
    Endpoint: commentanalyzer.googleapis.com
    """
    if api_key is None:
        api_key = get_perspective_api_key()

    if attributes is None:
        attributes = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "INSULT",
            "PROFANITY",
            "THREAT",
        ]

    if languages is None:
        languages = ["en"]

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
        "languages": languages,
        "doNotStore": True,
    }

    params = {"key": api_key}
    headers = {"Content-Type": "application/json"}

    response = requests.post(
        PERSPECTIVE_API_URL,
        headers=headers,
        params=params,
        json=payload,
    )
    response.raise_for_status()
    return response.json()


def check_labels_safety(
    labels: List[DetectedLabel],
    *,
    api_key: Optional[str] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Check all detected labels for unsafe text content via Perspective API.
    """
    results: Dict[str, Dict[str, Any]] = {}
    for label in labels:
        if label.name and label.name.strip():
            safety = check_text_safety(label.name, api_key=api_key)
            results[label.name] = safety
    return results


def check_text_regions_safety(
    text_regions: List[DetectedTextRegion],
    *,
    api_key: Optional[str] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Check all detected text regions for unsafe content via Perspective API.
    """
    results: Dict[str, Dict[str, Any]] = {}
    for region in text_regions:
        if region.text and region.text.strip():
            safety = check_text_safety(region.text, api_key=api_key)
            results[region.text] = safety
    return results


def format_safety_report(safety_results: Dict[str, Dict[str, Any]]) -> str:
    """Format text safety check results into a human-readable report."""
    if not safety_results:
        return "No text content to evaluate."

    lines = ["Text Safety Assessment (Perspective API):"]
    for text, result in safety_results.items():
        scores = result.get("attributeScores", {})
        flags = []
        for attr_name, attr_data in scores.items():
            score = attr_data.get("summaryScore", {}).get("value", 0.0)
            if score > 0.5:
                flags.append(f"{attr_name}={score:.3f}")
        status = "FLAGGED" if flags else "OK"
        flags_str = f" - {', '.join(flags)}" if flags else ""
        lines.append(f"  [{status}] \"{text}\"{flags_str}")
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python visual_safety_text.py <text_to_check> [additional_text ...]")
        sys.exit(1)

    texts = sys.argv[1:]
    results = {}
    for text in texts:
        safety = check_text_safety(text)
        results[text] = safety

    report = format_safety_report(results)
    print(report)


if __name__ == "__main__":
    main()
