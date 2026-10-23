# observability_models.py

from typing import Any, Dict, List

# Request model skeleton for metric queries (common fields)
RequestModel = Dict[str, Any]

# Normalized response model for metric data (common across providers)
NormalizedMetricResponse = Dict[str, Any]

# Basic helper to convert provider‑specific payloads to the normalized schema


def normalize_response(provider_response: Dict[str, Any]) -> NormalizedMetricResponse:
    """Map provider‑specific response to a common normalized format."""
    # Example mapping for IBM Cloud Monitoring (add other providers as needed)
    if "datapoints" in provider_response:
        return {
            "metric": provider_response.get("metric_name"),
            "datapoints": [
                {"timestamp": dp.get("timestamp"), "value": dp.get("value")}
                for dp in provider_response.get("datapoints", [])
            ],
            "annotations": provider_response.get("annotations", []),
        }
    # Placeholder for other providers
    return provider_response


# Model for dimension / label filters (used by later-step files)
DimensionFilter = Dict[str, Any]

# Example: a filter expressed as {"resource_id":"i-123","region":"us-east-1"}
