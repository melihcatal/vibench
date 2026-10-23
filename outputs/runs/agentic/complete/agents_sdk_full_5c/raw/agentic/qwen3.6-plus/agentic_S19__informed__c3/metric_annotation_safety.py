"""Check free-text metric labels or annotations for unsafe text.

Uses Google Perspective API (requests-based REST integration) to
analyze metric annotations, dashboard notes, or custom labels for
toxicity, profanity, and other safety attributes.

Required environment:
    PERSPECTIVE_API_KEY - Google Perspective API key
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

import requests

from observability_client import ObservabilityClient
from observability_models import MetricSeries

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def build_annotation_list(
    series_list: List[MetricSeries],
) -> List[str]:
    """Extract all text labels/annotations from metric series."""
    annotations = []
    for s in series_list:
        for label_name, label_value in s.resource_labels.items():
            if isinstance(label_value, str):
                annotations.append(f"resource.{label_name}: {label_value}")
        for label_name, label_value in s.metric_labels.items():
            if isinstance(label_value, str):
                annotations.append(f"metric.{label_name}: {label_value}")
    return annotations


def check_annotation_safety(
    text: str,
    perspective_api_key: Optional[str] = None,
    requested_attributes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Check a single text annotation for safety using Perspective API.

    Sends the text to Google Perspective API commentanalyzer endpoint
    with the specified toxicity and safety attributes.
    """
    api_key = perspective_api_key or os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY must be set")

    attributes = requested_attributes or [
        "TOXICITY",
        "SEVERE_TOXICITY",
        "IDENTITY_ATTACK",
        "INSULT",
        "PROFANITY",
        "THREAT",
    ]

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
        "languages": ["en"],
    }

    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def check_metric_annotations_safety(
    metric_type: str,
    project_id: Optional[str] = None,
    minutes: int = 60,
    threshold: float = 0.5,
    perspective_api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Check all annotations from a metric query for unsafe content.

    Queries Google Cloud Monitoring for metric series, extracts
    text labels, and checks each with Perspective API.

    Args:
        metric_type: GCP metric type
        project_id: GCP project ID
        minutes: Lookback window
        threshold: Score above which a label is flagged
        perspective_api_key: Perspective API key

    Returns:
        Dict with flagged annotations and their scores.
    """
    client = ObservabilityClient(project_id=project_id)
    series_list = client.query_metric_window(metric_type, minutes=minutes)

    annotations = build_annotation_list(series_list)
    if not annotations:
        return {"status": "no_annotations", "flagged": [], "checked": 0}

    flagged = []
    checked = 0

    for annotation in annotations:
        result = check_annotation_safety(annotation, perspective_api_key=perspective_api_key)
        checked += 1

        attribute_scores = result.get("attributeScores", {})
        for attr_name, attr_data in attribute_scores.items():
            score = attr_data.get("summaryScore", {}).get("value", 0.0)
            if score >= threshold:
                flagged.append({
                    "annotation": annotation,
                    "attribute": attr_name,
                    "score": score,
                })

    return {
        "status": "complete",
        "checked": checked,
        "flagged": flagged,
        "flagged_count": len(flagged),
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Check metric annotations via Perspective API")
    parser.add_argument("--metric-type", required=True, help="GCP metric type")
    parser.add_argument("--project-id", default=None)
    parser.add_argument("--minutes", type=int, default=60)
    parser.add_argument("--threshold", type=float, default=0.5, help="Flag threshold")
    args = parser.parse_args()

    results = check_metric_annotations_safety(
        metric_type=args.metric_type,
        project_id=args.project_id,
        minutes=args.minutes,
        threshold=args.threshold,
    )
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
