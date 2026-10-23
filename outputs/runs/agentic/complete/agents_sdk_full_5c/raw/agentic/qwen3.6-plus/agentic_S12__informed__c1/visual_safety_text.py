"""
visual_safety_text.py - Check generated visual labels for unsafe text
using Google Perspective API.

Provider: Perspective API
SDK: requests (REST interface)
Auth: PERSPECTIVE_API_KEY
API Host: commentanalyzer.googleapis.com
"""

import os
import sys
import json
from typing import List, Dict, Any, Optional

import requests


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_text_safety(
    text: str,
    attributes: Optional[List[str]] = None,
    languages: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Check a text string (such as detected image text or generated labels)
    for toxic or unsafe content using the Perspective API.

    Args:
        text: The text to analyze for safety/toxicity.
        attributes: List of attributes to score. Defaults to common toxicity attributes.
        languages: List of language codes. Defaults to ["en"].

    Returns:
        Dict with attribute scores and analysis metadata.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError(
            "PERSPECTIVE_API_KEY environment variable must be set "
            "for Perspective API access."
        )

    if attributes is None:
        attributes = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "INSULT",
            "PROFANITY",
            "THREAT",
            "SEXUALLY_EXPLICIT",
        ]

    if languages is None:
        languages = ["en"]

    requested_attributes = {attr: {} for attr in attributes}

    payload = {
        "comment": {"text": text},
        "languages": languages,
        "requestedAttributes": requested_attributes,
    }

    params = {"key": api_key}
    headers = {"Content-Type": "application/json"}

    response = requests.post(
        PERSPECTIVE_API_URL,
        params=params,
        headers=headers,
        json=payload,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Perspective API request failed: {response.status_code} - {response.text}"
        )

    result = response.json()
    return result


def get_safety_scores(
    analysis_result: Dict[str, Any],
) -> Dict[str, float]:
    """
    Extract numerical safety scores from the Perspective API response.

    Returns a dict mapping attribute names to their summary scores (0.0 to 1.0).
    """
    scores = {}
    attribute_scores = analysis_result.get("attributeScores", {})

    for attr_name, attr_data in attribute_scores.items():
        summary = attr_data.get("summaryScore", {})
        scores[attr_name] = round(summary.get("value", 0.0), 4)

    return scores


def assess_text_safety(
    analysis_result: Dict[str, Any],
    threshold: float = 0.5,
) -> Dict[str, Any]:
    """
    Assess whether text is safe based on Perspective API scores.

    Args:
        analysis_result: The raw API response.
        threshold: Score above which content is flagged.

    Returns:
        Dict with is_safe, highest_score, flagged_attributes, and scores.
    """
    scores = get_safety_scores(analysis_result)

    flagged = {attr: score for attr, score in scores.items() if score >= threshold}
    is_safe = len(flagged) == 0

    highest_score = max(scores.values()) if scores else 0.0
    highest_attr = max(scores, key=scores.get) if scores else "N/A"

    return {
        "is_safe": is_safe,
        "highest_score": highest_score,
        "highest_attribute": highest_attr,
        "flagged_attributes": flagged,
        "all_scores": scores,
    }


def check_labels_for_safety(
    labels: List[str],
    attributes: Optional[List[str]] = None,
    threshold: float = 0.5,
) -> List[Dict[str, Any]]:
    """
    Check a list of visual labels or descriptions for text safety issues.

    Args:
        labels: List of label strings to check.
        attributes: Perspective API attributes to score.
        threshold: Safety threshold for flagging.

    Returns:
        List of assessment dicts for each label.
    """
    results = []
    for label in labels:
        if not label.strip():
            continue
        try:
            analysis = check_text_safety(label, attributes=attributes)
            assessment = assess_text_safety(analysis, threshold=threshold)
            assessment["label"] = label
            results.append(assessment)
        except Exception as e:
            results.append({
                "label": label,
                "error": str(e),
                "is_safe": False,
            })
    return results


def main():
    """CLI entry point for checking text safety of visual labels."""
    if len(sys.argv) < 2:
        print("Usage: python visual_safety_text.py '<text to check>' [threshold]")
        sys.exit(1)

    text = sys.argv[1]
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    try:
        analysis = check_text_safety(text)
        assessment = assess_text_safety(analysis, threshold=threshold)

        print(f"Text Safety Assessment")
        print(f"{'=' * 40}")
        print(f"Input: {text}")
        print(f"Overall safe: {assessment['is_safe']}")
        print(f"Highest score: {assessment['highest_score']} ({assessment['highest_attribute']})")

        if assessment["flagged_attributes"]:
            print(f"\nFlagged attributes (threshold >= {threshold}):")
            for attr, score in assessment["flagged_attributes"].items():
                print(f"  - {attr}: {score}")
        else:
            print(f"\nNo attributes exceeded the safety threshold.")
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
