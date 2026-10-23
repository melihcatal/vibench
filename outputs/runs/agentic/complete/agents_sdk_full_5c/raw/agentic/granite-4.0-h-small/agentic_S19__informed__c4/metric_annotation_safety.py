# [LATER-STEP] metric_annotation_safety.py
# Check free-text metric labels or annotations for unsafe text using Tisane moderation API

import os
import requests
from observability_client import get_monitoring_client
from observability_models import TimeInterval
from typing import Dict

# Provider SDK import - provider identifiable
import tisane

TISANE_API_KEY = os.getenv("TISANE_API_KEY")
BASE_URL = "https://api.tisane.ai/v1/parse"

def metric_annotation_safety(metric_type: str, window_minutes: int = 60, **labels) -> Dict[str, Any]:
    """Inspect recent metric label values for unsafe or policy‑violating content.

    Args:
        metric_type: Fully qualified metric type (e.g., "custom.googleapis.com/my/metric").
        window_minutes: Lookback window.
        **labels: Dimension filters to isolate resources.

    Returns:
        Dictionary with Tisane API response details.
    """
    client = get_monitoring_client()
    end_ts = int(datetime.now().timestamp())
    start_ts = end_ts - 60 * window_minutes
    interval = TimeInterval.from_seconds(start_ts, end_ts)
    request = {
        "name": client.project_path(),
        "metric_type": metric_type,
        "interval": interval,
        "filter_": f"labels.{next(iter(labels))}='{labels[next(iter(labels))]}"
        if labels else ""
    }
    # Collect label values from recent time series (naïve assumption: label values are constant over interval)
    label_values: List[str] = []
    for ts in client.list_time_series(request):
        # Assuming the label value is part of the metric's metadata; we pull it from the descriptor
        descriptor = client.get_metric_descriptor(metric_type)
        # Extract relevant label definitions (value descriptions)
        for label in descriptor.label_descriptors:
            # Placeholder: in real code we would map the label key to its recent value from points
            # Here we just include the label key as a stand‑in for its value
            label_values.append(label.key)
    # 2. Moderate content via Tisane
    settings = {
        "languages": "en",
        "flags": ["moderation"],
        "settings": {
            "moderation": {
                "categories": ["toxic", "hate", "self_harm", "sexual", "political"]
            }
        }
    }
    headers = {
        "Authorization": f"Bearer {TISANE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": " \n".join(label_values),
        **settings
    }
    resp = requests.post(BASE_URL, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()
