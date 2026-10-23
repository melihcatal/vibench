from typing import Optional

from translation_client import check_content_safety
from translation_models import UnsafeContentFlag, UnsafeContentReport


GOOGLE_PERSPECTIVE_API_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)

UNSAFE_CATEGORIES = {
    "TOXICITY": 0.7,
    "SEVERE_TOXICITY": 0.5,
    "INSULT": 0.6,
    "PROFANITY": 0.6,
    "THREAT": 0.4,
}


def check_unsafe_copy(
    texts: list[str],
    api_key: Optional[str] = None,
    thresholds: Optional[dict[str, float]] = None,
) -> UnsafeContentReport:
    flags: list[UnsafeContentFlag] = []
    effective_thresholds = thresholds or UNSAFE_CATEGORIES

    for i, text in enumerate(texts):
        try:
            response_data = check_content_safety(text=text, api_key=api_key)
            segment_flags = _parse_safety_response(
                response_data, text, i, effective_thresholds
            )
            flags.extend(segment_flags)
        except Exception:
            continue

    return UnsafeContentReport(
        has_unsafe_content=len(flags) > 0,
        flags=flags,
    )


def _parse_safety_response(
    response_data: dict,
    text: str,
    segment_index: int,
    thresholds: dict[str, float],
) -> list[UnsafeContentFlag]:
    flags: list[UnsafeContentFlag] = []
    attribute_scores = response_data.get("attributeScores", {})

    for category, threshold in thresholds.items():
        if category in attribute_scores:
            score_summary = attribute_scores[category].get("summaryScore", {})
            value = score_summary.get("value", 0.0)
            if value >= threshold:
                flags.append(
                    UnsafeContentFlag(
                        category=category,
                        confidence=round(value, 4),
                        flagged_text=text,
                        segment_index=segment_index,
                    )
                )

    return flags


def check_single_text_unsafe(
    text: str,
    api_key: Optional[str] = None,
    thresholds: Optional[dict[str, float]] = None,
) -> UnsafeContentReport:
    return check_unsafe_copy(
        texts=[text],
        api_key=api_key,
        thresholds=thresholds,
    )


def get_unsafe_categories_report(
    texts: list[str],
    api_key: Optional[str] = None,
) -> dict[str, int]:
    report = check_unsafe_copy(texts=texts, api_key=api_key)
    category_counts: dict[str, int] = {}
    for flag in report.flags:
        category_counts[flag.category] = category_counts.get(flag.category, 0) + 1
    return category_counts
