# metric_annotation_safety.py

from __future__ import annotations

import json
from typing import Any, Dict, List

from observability_client import get_metrics_client
from observability_models import DimensionFilter

# ---------------------------------------------------------------------------
# Configuration (choose ONE concrete provider)
# ---------------------------------------------------------------------------
# Example: IBM Cloud Monitoring
IBM_MONITORING_INSTANCE_ID = "YOUR_MONITORING_INSTANCE_ID"
IBM_CLOUD_API_KEY = "YOUR_IBM_CLOUD_API_KEY"

# Example: Amazon CloudWatch Metrics (uncomment if using AWS)
# AWS_ACCESS_KEY_ID = "YOUR_AWS_ACCESS_KEY_ID"
# AWS_SECRET_ACCESS_KEY = "YOUR_AWS_SECRET_ACCESS_KEY"

# ---------------------------------------------------------------------------
# Helper: retrieve raw annotation strings for a metric over a window
# ---------------------------------------------------------------------------


def fetch_annotations(
    metric_name: str, start: int, end: int, filters: List[DimensionFilter] = None
) -> List[str]:
    """Pull raw text annotations/labels attached to a metric in the given window."""
    client = get_metrics_client()
    raw = client.query(
        payload={"metric": metric_name, "start": start, "end": end, "filters": filters}
    )
    # Assuming provider returns an "annotations" list of dicts with a "text" field
    return [item.get("text", "") for item in raw.get("annotations", [])]


# ---------------------------------------------------------------------------
# Safety check using hosted LLM (Watsonx Guardrails example)
# ---------------------------------------------------------------------------


def is_safe(annotation: str) -> bool:
    """Call a hosted moderation/guardrails service to detect unsafe language.
    Returns True if safe, False otherwise.
    """
    # Placeholder: the actual call would be client.moderate(text=annotation) or an HTTP request
    # For illustration, we'll assume watsonx.ai guardrails endpoint is exposed via client
    moderation = client.moderate(text=annotation)
    # Expected moderation response has a boolean "safe" flag
    return moderation.get("safe", False)


# ---------------------------------------------------------------------------
# Core function to evaluate all annotations for a metric
# ---------------------------------------------------------------------------
def metric_annotation_safety(
    metric_name: str, start: int, end: int, filters: List[DimensionFilter] = None
) -> Dict[str, Any]:
    annotations = fetch_annotations(metric_name, start, end, filters)
    unsafe = [txt for txt in annotations if not is_safe(txt)]
    return {
        "metric": metric_name,
        "total_annotations": len(annotations),
        "unsafe_annotations": unsafe,
        "is_all_safe": len(unsafe) == 0,
    }


# ---------------------------------------------------------------------------
# Example usage (for local testing only)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import time

    now = int(time.time())
    five_min_ago = now - 300
    filters = [{"resource_id": "i-0abcd1234"}]
    result = metric_annotation_safety(
        "disk.io.rate", start=five_min_ago, end=now, filters=filters
    )
    print(json.dumps(result, indent=2))
