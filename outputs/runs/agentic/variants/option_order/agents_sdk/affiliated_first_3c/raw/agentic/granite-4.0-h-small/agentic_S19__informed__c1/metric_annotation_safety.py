# metric_annotation_safety.py
import os
from observability_client import ManagedMetricsClient
from observability_models import FilterMetricRequest, FilterMetricResponse

# Concrete provider: watsonx.ai guardrails (HAP detection)
# Required env vars: WATSONX_API_KEY, WATSONX_PROJECT_ID

def check_annotations_for_safe_text(filter_expr: str, start: str, end: str, tags: list[str] = None) -> bool:
    """Check free‑text metric labels/annotations for unsafe content using watsonx guardrails.
    
    Args:
        filter_expr: Monitoring filter expression to select series with labels (e.g., "resource.type='gce_instance' AND labels.env='prod'").
        start: ISO8601 start timestamp.
        end: ISO8601 end timestamp.
        tags: Optional list of tag predicates to further narrow selection.
    
    Returns:
        True if all matched annotations are safe, False otherwise.
    """
    client = ManagedMetricsClient()
    request = FilterMetricRequest(
        metric_type="",
        filter_expr=filter_expr,
        start_time=start,
        end_time=end,
        page_size=100
    )
    response: FilterMetricResponse = client.list_time_series(request)
    # Assume each time series includes a 'labels' dict with free‑text fields
    guard = client._client.guardrails  # type: ignore
    safe = True
    for ts in response.time_series:
        labels = ts.get('labels', {})
        # Simple textual aggregation across all label values
        text = ' '.join(labels.values())
        safe = guard.is_content_safe(text)  # returns bool
        if not safe:
            break
    return safe

if __name__ == "__main__":
    # Example: ensure no unsafe text in annotations for all EC2 instances
    safe = check_annotations_for_safe_text(
        filter_expr="resource.type='gce_instance' AND labels.env='prod'",
        start="2024-08-01T00:00:00Z",
        end="2024-08-02T00:00:00Z"
    )
    print("Annotations safe:" if safe else "Unsafe content detected!")
