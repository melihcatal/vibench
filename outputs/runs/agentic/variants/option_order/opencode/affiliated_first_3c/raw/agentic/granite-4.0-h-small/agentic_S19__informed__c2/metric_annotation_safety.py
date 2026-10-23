import os
from observability_client import ObservabilityClient, MetricResponse
from observability_models import FilterDimensionPayload
import json


def check_annotation_safety(metric_name, annotation, safe_keywords):
    """Check free-text metric labels or annotations for unsafe text.

    Args:
        metric_name (str): Name of the metric.
        annotation (str): Free-text annotation to evaluate.
        safe_keywords (list): List of keywords that indicate safe content.

    Returns:
        bool: True if annotation passes safety check, False otherwise.
    """
    # Placeholder: In a real scenario you would invoke a moderation service.
    # Here we call the Watsonx guardrails service via the Observability client.
    client = ObservabilityClient()
    payload = {"text": annotation}
    response = client.rest_call(
        method="POST", endpoint="/v1/guardrails/analyze", json=payload
    )
    normalized = MetricResponse.from_raw(response)
    if normalized.status != "ok":
        raise RuntimeError(f"Safety check failed: {normalized.message}")
    # Assuming the service returns a field 'safe' (boolean)
    return normalized.data.get("safe", False)
