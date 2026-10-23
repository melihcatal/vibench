from typing import List, Optional

from observability_client import ObservabilityClient
from observability_models import SafetyCheckResult

TOXIC_CATEGORIES = [
    "HATE_SPEECH",
    "GRAPHIC_VIOLENCE",
    "HARASSMENT",
    "SELF_HARM",
    "SEXUAL",
    "PROFANITY",
]

DEFAULT_SAFETY_THRESHOLD = 0.5


def metric_annotation_safety(
    text: str,
    categories: Optional[List[str]] = None,
    threshold: float = DEFAULT_SAFETY_THRESHOLD,
    region: Optional[str] = None,
) -> SafetyCheckResult:
    client = ObservabilityClient(region=region)

    response = client.detect_toxic_content(text=text)

    detected_categories = []
    confidence_scores = {}

    results = response.get("ResultList", [])
    for result in results:
        matches = result.get("Matches", [])
        for match in matches:
            category = match.get("Type", "")
            score = match.get("Score", 0.0)
            confidence_scores[category] = score

            if score >= threshold:
                if category not in detected_categories:
                    detected_categories.append(category)

    is_safe = len(detected_categories) == 0

    return SafetyCheckResult(
        text=text,
        is_safe=is_safe,
        categories=detected_categories,
        confidence_scores=confidence_scores,
    )


def batch_annotation_safety(
    texts: List[str],
    categories: Optional[List[str]] = None,
    threshold: float = DEFAULT_SAFETY_THRESHOLD,
    region: Optional[str] = None,
) -> List[SafetyCheckResult]:
    results = []
    for text in texts:
        result = metric_annotation_safety(
            text=text,
            categories=categories,
            threshold=threshold,
            region=region,
        )
        results.append(result)
    return results


def format_safety_results(results: List[SafetyCheckResult]) -> str:
    lines = []
    for result in results:
        status = "SAFE" if result.is_safe else "UNSAFE"
        lines.append(f"[{status}] Text: {result.text[:80]}...")
        if result.categories:
            for category in result.categories:
                score = result.confidence_scores.get(category, 0.0)
                lines.append(f"  - {category}: {score:.4f}")
        lines.append("")
    return "\n".join(lines)
