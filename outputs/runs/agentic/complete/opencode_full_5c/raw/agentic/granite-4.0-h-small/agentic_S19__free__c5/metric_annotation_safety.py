# [LATER-STEP] metric_annotation_safety.py

# Check free‑text metric labels or annotations for unsafe text using New Relic as provider.

from __future__ import annotations
from typing import List
import re
import json

from observability_client import NewRelicClient
from observability_models import FilteredMetricRequest, FilteredMetricResponse

UNSAFE_PATTERNS = [
    re.compile(r"password", re.IGNORECASE),
    re.compile(r"secret", re.IGNORECASE),
    re.compile(r"credential", re.IGNORECASE),
    re.compile(r"key", re.IGNORECASE),
]


def contains_unsafe_text(text: str) -> bool:
    """Return True if any unsafe regex pattern matches the text."""
    return any(p.search(text) for p in UNSAFE_PATTERNS)


def check_annotations_for_unsafe(metric_name: str) -> List[str]:
    """
    Retrieve all annotations/labels for a metric and return a list of annotation IDs
    that contain unsafe words.

    New Relic does not expose a dedicated “annotations” endpoint, so as an example we
    query a custom attribute collection that stores metric labels.
    """
    # Pretend the attribute set is named `metric_labels`
    payload = FilteredMetricRequest(
        metric=metric_name,
        start=datetime.utcnow()
        - timedelta(days=365),  # fetch any label attached to the metric
        end=datetime.utcnow(),
        dimensions={"label_type": ["annotation"]},
    )
    client = NewRelicClient()
    raw: Dict[str, Any] = client.query_filtered_metrics(payload.__dict__)
    # Normalize the payload using our model (simulated here)
    normalized: FilteredMetricResponse = FilteredMetricResponse.from_dict(raw)
    unsafe_annotations = []
    for label in normalized.datapoints:
        # Assume each datapoint carries a `value` field that holds the free‑text label
        label_text = label.get("value", "")
        if contains_unsafe_text(label_text):
            unsafe_annotations.append(label.get("id", f"unknown_{label_text}"))
    return unsafe_annotations


if __name__ == "__main__":
    unsafe = check_annotations_for_unsafe("request.rate")
    print(
        json.dumps({"metric": "request.rate", "unsafe_annotations": unsafe}, indent=2)
    )
