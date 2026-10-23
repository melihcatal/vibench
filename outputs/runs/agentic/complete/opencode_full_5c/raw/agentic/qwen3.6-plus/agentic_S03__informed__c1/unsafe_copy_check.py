import os
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import requests


@dataclass
class SafetyAttribute:
    name: str
    score: float
    threshold: float
    flagged: bool


@dataclass
class SafetyCheckResult:
    text: str
    attributes: List[SafetyAttribute] = field(default_factory=list)
    overall_safe: bool = True
    flagged_attributes: List[str] = field(default_factory=list)


@dataclass
class UnsafeCopyReport:
    results: List[SafetyCheckResult] = field(default_factory=list)
    total_flagged: int = 0
    summary: str = ""


def check_unsafe_copy(
    texts: List[str],
    attributes: Optional[List[str]] = None,
    threshold: float = 0.7,
) -> UnsafeCopyReport:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set")

    if attributes is None:
        attributes = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "INSULT",
            "PROFANITY",
            "THREAT",
            "SEXUALLY_EXPLICIT",
            "IDENTITY_ATTACK",
        ]

    perspective_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    results = []
    total_flagged = 0

    for text in texts:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {attr: {} for attr in attributes},
            "languages": ["en"],
            "doNotStore": True,
        }

        params = {"key": api_key}
        headers = {"Content-Type": "application/json"}

        response = requests.post(
            perspective_url,
            json=payload,
            params=params,
            headers=headers,
        )
        response.raise_for_status()
        data = response.json()

        attribute_scores = data.get("attributeScores", {})
        safety_attributes = []
        flagged_attrs = []
        overall_safe = True

        for attr_name, attr_data in attribute_scores.items():
            score = attr_data.get("summaryScore", {}).get("value", 0.0)
            flagged = score >= threshold
            safety_attr = SafetyAttribute(
                name=attr_name,
                score=score,
                threshold=threshold,
                flagged=flagged,
            )
            safety_attributes.append(safety_attr)
            if flagged:
                overall_safe = False
                flagged_attrs.append(attr_name)

        check_result = SafetyCheckResult(
            text=text,
            attributes=safety_attributes,
            overall_safe=overall_safe,
            flagged_attributes=flagged_attrs,
        )
        results.append(check_result)
        if not overall_safe:
            total_flagged += 1

    flagged_texts = [r.text for r in results if not r.overall_safe]
    if total_flagged == 0:
        summary = "All texts passed safety checks."
    else:
        summary = (
            f"{total_flagged} of {len(texts)} texts flagged for unsafe content. "
            f"Flagged attributes: {', '.join(set(a for r in results for a in r.flagged_attributes))}"
        )

    return UnsafeCopyReport(
        results=results,
        total_flagged=total_flagged,
        summary=summary,
    )
