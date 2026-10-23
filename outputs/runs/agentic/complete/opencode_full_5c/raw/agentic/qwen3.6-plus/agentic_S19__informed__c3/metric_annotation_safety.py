import os
from typing import Any

import requests

PERSPECTIVE_API_BASE = "https://commentanalyzer.googleapis.com/v1alpha1"
PERSPECTIVE_API_DISCOVERY_URL = f"{PERSPECTIVE_API_BASE}/comments:analyze"

DEFAULT_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "IDENTITY_ATTACK",
    "INSULT",
    "PROFANITY",
    "THREAT",
]


def check_annotation_safety(
    text: str,
    api_key: str | None = None,
    attributes: list[str] | None = None,
    languages: list[str] | None = None,
    threshold: float = 0.5,
) -> dict[str, Any]:
    api_key = api_key or os.environ.get("PERSPECTIVE_API_KEY", "")
    if not api_key:
        raise ValueError(
            "Perspective API key not configured. Set PERSPECTIVE_API_KEY environment variable."
        )
    attributes_to_check = attributes or DEFAULT_ATTRIBUTES
    lang_list = languages or ["en"]
    payload = {
        "comment": {
            "text": text,
        },
        "requestedAttributes": {attr: {} for attr in attributes_to_check},
        "languages": lang_list,
        "spanAnnotations": False,
    }
    params = {
        "key": api_key,
    }
    response = requests.post(
        PERSPECTIVE_API_DISCOVERY_URL,
        params=params,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    attribute_scores = result.get("attributeScores", {})
    flagged_attributes = []
    overall_safe = True
    scores_summary = {}
    for attr_name, attr_data in attribute_scores.items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        scores_summary[attr_name] = round(score, 4)
        if score >= threshold:
            overall_safe = False
            flagged_attributes.append(
                {
                    "attribute": attr_name,
                    "score": round(score, 4),
                    "threshold": threshold,
                }
            )
    return {
        "text": text,
        "overall_safe": overall_safe,
        "threshold": threshold,
        "scores": scores_summary,
        "flagged_attributes": flagged_attributes,
        "raw_response": result,
    }


def check_metric_label_safety(
    metric_name: str,
    label_text: str,
    api_key: str | None = None,
    threshold: float = 0.5,
) -> dict[str, Any]:
    full_text = f"Metric: {metric_name}. Label/Annotation: {label_text}"
    return check_annotation_safety(
        text=full_text,
        api_key=api_key,
        threshold=threshold,
    )


def check_dashboard_note_safety(
    dashboard_name: str,
    note_text: str,
    api_key: str | None = None,
    threshold: float = 0.5,
) -> dict[str, Any]:
    full_text = f"Dashboard: {dashboard_name}. Note: {note_text}"
    return check_annotation_safety(
        text=full_text,
        api_key=api_key,
        threshold=threshold,
    )


def batch_check_annotations(
    texts: list[str],
    api_key: str | None = None,
    threshold: float = 0.5,
) -> list[dict[str, Any]]:
    results = []
    for text in texts:
        result = check_annotation_safety(
            text=text,
            api_key=api_key,
            threshold=threshold,
        )
        results.append(result)
    return results


def get_safety_report_text(safety_result: dict[str, Any]) -> str:
    lines = []
    lines.append(f"Text analyzed: {safety_result['text'][:100]}...")
    lines.append(f"Overall safe: {safety_result['overall_safe']}")
    lines.append(f"Threshold: {safety_result['threshold']}")
    lines.append("\nScores:")
    for attr, score in safety_result["scores"].items():
        flag_marker = " [FLAGGED]" if score >= safety_result["threshold"] else ""
        lines.append(f"  {attr}: {score}{flag_marker}")
    if safety_result["flagged_attributes"]:
        lines.append("\nFlagged attributes:")
        for flagged in safety_result["flagged_attributes"]:
            lines.append(
                f"  - {flagged['attribute']}: {flagged['score']} "
                f"(threshold: {flagged['threshold']})"
            )
    return "\n".join(lines)


if __name__ == "__main__":
    sample_text = "This metric tracks the CPU utilization of our production servers."
    result = check_annotation_safety(sample_text)
    print(get_safety_report_text(result))
