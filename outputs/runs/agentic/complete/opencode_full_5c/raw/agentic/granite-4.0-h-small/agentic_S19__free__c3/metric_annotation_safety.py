# LATER-STEP
# metric_annotation_safety.py
# Inspect free‑text metric labels/annotations for unsafe content using Datadog as the managed metrics provider

import re
from observability_client import get_datadog_client
from observability_models import MetricQueryRequest, MetricQueryResponse
from typing import Optional

def contains_sensitive_content(annotation: str) -> Optional[str]:
    """Naïve check for potentially unsafe text (e.g., PII, profanity)."
    # Simple regex patterns – replace with a more sophisticated detector in production
    pii_pattern = re.compile(r"\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b")  # SSN-like
    profanity = re.compile(r"\b(damn|hell|crap)\b", re.IGNORECASE)
    if pii_pattern.search(annotation):
        return "contains SSN-like pattern"
    if profanity.search(annotation):
        return "contains profanity"
    return None

def check_metric_annotations(metric: str, start: str, end: str) -> list:
    """
    Retrieve recent metric annotations (notes) for a metric and flag unsafe entries.
    
    Args:
        metric (str): Datadog metric name.
        start (str): RFC3339 start of window.
        end (str): RFC3339 end of window.
    
    Returns:
        list: Dicts with annotation text and a 'safety_flag' field if unsafe.
    """
    client = get_datadog_client()
    # Datadog does not have a dedicated annotations API; we simulate by querying events tied to the metric.
    # Here we just demonstrate a placeholder call.
    request = MetricQueryRequest(query=metric, start=start, end=end, limit=10)
    raw = client.query_metrics(request)  # placeholder – real code would use Datadog Event API
    # Assume raw contains an 'annotations' field (pseudo‑code)
    annotations = raw.get("annotations", [])
    results = []
    for ann in annotations:
        flag = contains_sensitive_content(ann.get("text", ""))
        results.append({
            "text": ann.get("text"),
            "timestamp": ann.get("timestamp"),
            "safety_flag": flag,
        })
    return results
