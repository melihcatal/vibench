import os
import requests
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ToxicityCategory(str, Enum):
    TOXICITY = "TOXICITY"
    SEVERE_TOXICITY = "SEVERE_TOXICITY"
    IDENTITY_ATTACK = "IDENTITY_ATTACK"
    INSULT = "INSULT"
    PROFANITY = "PROFANITY"
    THREAT = "THREAT"
    SEXUALLY_EXPLICIT = "SEXUALLY_EXPLICIT"
    FLIRTATION = "FLIRTATION"


@dataclass
class SafetyScore:
    category: ToxicityCategory
    score: float
    threshold: float
    is_unsafe: bool


@dataclass
class SafetyCheckResult:
    text: str
    overall_safe: bool
    scores: List[SafetyScore]
    languages: List[str]
    flagged_categories: List[str]


def check_text_safety(
    text: str,
    categories: Optional[List[ToxicityCategory]] = None,
    thresholds: Optional[Dict[ToxicityCategory, float]] = None,
) -> SafetyCheckResult:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    if categories is None:
        categories = [
            ToxicityCategory.TOXICITY,
            ToxicityCategory.SEVERE_TOXICITY,
            ToxicityCategory.IDENTITY_ATTACK,
            ToxicityCategory.INSULT,
            ToxicityCategory.PROFANITY,
            ToxicityCategory.THREAT,
            ToxicityCategory.SEXUALLY_EXPLICIT,
        ]

    if thresholds is None:
        thresholds = {
            ToxicityCategory.TOXICITY: 0.7,
            ToxicityCategory.SEVERE_TOXICITY: 0.8,
            ToxicityCategory.IDENTITY_ATTACK: 0.7,
            ToxicityCategory.INSULT: 0.7,
            ToxicityCategory.PROFANITY: 0.7,
            ToxicityCategory.THREAT: 0.7,
            ToxicityCategory.SEXUALLY_EXPLICIT: 0.7,
            ToxicityCategory.FLIRTATION: 0.7,
        }

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    requested_attributes = {}
    for category in categories:
        requested_attributes[category.value] = {}

    payload = {
        "comment": {"text": text},
        "requestedAttributes": requested_attributes,
        "languages": ["en", "es", "fr", "de", "it", "pt", "ru"],
    }

    params = {"key": api_key}

    try:
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        data = response.json()

        scores = []
        flagged_categories = []

        for category in categories:
            if category.value in data.get("attributeScores", {}):
                attribute_data = data["attributeScores"][category.value]
                score = attribute_data.get("summaryScore", {}).get("value", 0.0)
                threshold = thresholds.get(category, 0.7)
                is_unsafe = score > threshold

                safety_score = SafetyScore(
                    category=category,
                    score=score,
                    threshold=threshold,
                    is_unsafe=is_unsafe,
                )
                scores.append(safety_score)

                if is_unsafe:
                    flagged_categories.append(category.value)

        overall_safe = len(flagged_categories) == 0

        detected_languages = data.get("languages", [])

        return SafetyCheckResult(
            text=text,
            overall_safe=overall_safe,
            scores=scores,
            languages=detected_languages,
            flagged_categories=flagged_categories,
        )

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to check text safety: {str(e)}")


def batch_check_safety(
    texts: List[str],
    categories: Optional[List[ToxicityCategory]] = None,
    thresholds: Optional[Dict[ToxicityCategory, float]] = None,
) -> List[SafetyCheckResult]:
    results = []
    for text in texts:
        result = check_text_safety(text, categories, thresholds)
        results.append(result)
    return results


def check_translated_copy_safety(
    original_text: str, translated_text: str, target_lang: str
) -> Dict[str, Any]:
    original_result = check_text_safety(original_text)
    translated_result = check_text_safety(translated_text)

    comparison = {
        "original_safe": original_result.overall_safe,
        "translated_safe": translated_result.overall_safe,
        "original_flagged": original_result.flagged_categories,
        "translated_flagged": translated_result.flagged_categories,
        "safety_changed": original_result.overall_safe
        != translated_result.overall_safe,
        "new_issues_in_translation": [
            cat
            for cat in translated_result.flagged_categories
            if cat not in original_result.flagged_categories
        ],
    }

    return comparison


if __name__ == "__main__":
    test_text = "This is a sample text to check for safety issues."

    result = check_text_safety(test_text)

    print(f"Text: {result.text}")
    print(f"Overall safe: {result.overall_safe}")
    print(f"Detected languages: {result.languages}")
    print(f"Flagged categories: {result.flagged_categories}")

    for score in result.scores:
        print(
            f"  {score.category.value}: {score.score:.3f} (threshold: {score.threshold}, unsafe: {score.is_unsafe})"
        )
