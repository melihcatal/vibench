import os
import json
from datetime import datetime
from typing import List, Dict
import requests


def summarize_key_usage() -> Dict[str, Any]:
    api_key = os.getenv("GOOGLE_CLOUD_MONITORING_API_KEY")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    key_name = os.getenv("GOOGLE_KMS_KEY_NAME")

    if not all([api_key, project_id, key_name]):
        raise ValueError("Missing required Google Cloud environment variables")

    metric_type = "kms.googleapis.com/crypto.googleapis.com/cryptokey_version/crypto_operations_count"
    filter_str = f'metric.type="{metric_type}" AND resource.label.key_name="{key_name}"'

    url = f"https://monitoring.googleapis.com/v3/projects/{project_id}/timeSeries"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    params = {
        "filter": filter_str,
        "interval.endTime": datetime.utcnow().isoformat() + "Z",
        "interval.startTime": (datetime.utcnow() - timedelta(days=7)).isoformat() + "Z",
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    time_series = response.json().get("timeSeries", [])
    summary = {
        "key_id": key_name,
        "total_operations": sum(
            int(point["value"]["int64Value"])
            for ts in time_series
            for point in ts["points"]
        ),
        "operations_by_type": {},
        "time_range": {
            "start": params["interval.startTime"],
            "end": params["interval.endTime"],
        },
    }

    for ts in time_series:
        metric_kind = ts["metric"]["labels"]["crypto_operation"]
        summary["operations_by_type"][metric_kind] = sum(
            int(point["value"]["int64Value"]) for point in ts["points"]
        )

    return summary
