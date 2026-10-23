import os
from typing import Dict

# Managed Metrics Monitoring request/response models

# Example model for a metric query request
MetricQueryRequest = Dict[str, Any]


# Example response structure from the same-scenario client wrappers
def normalize_metric_response(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Convert raw CloudWatch get_metric_data response into a consistent dict format"""
    if not raw.get("MetricDataResults"):
        return {}
    result = raw["MetricDataResults"][0]
    return {
        "metric_name": result["Label"],
        "timestamps": result.get("Timestamps", []),
        "values": result.get("Values", []),
    }
