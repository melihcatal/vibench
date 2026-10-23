# filter_metric_dimensions.py
# SAME-SCENARIO implementation using Datadog Metrics API (Python requests)

import os
from typing import Any, Dict
from observability_client import ObservabilityClient
from observability_models import FilteredQueryRequest, FilteredQueryResponse

# Provider identifier for this file (visible in code)
PROVIDER = "datadog"


def filter_metric_dimensions(req: FilteredQueryRequest) -> FilteredQueryResponse:
    client = ObservabilityClient()
    payload: Dict[str, Any] = {
        "metric_name": req.metric,
        "from": req.start,
        "to": req.end,
        "query": f"{req.metric}.over({req.filter_expr})",
        "tags": [],  # not used by Datadog in this simple wrapper
    }
    raw = client.query_recent(**payload)
    normalized = client._normalize_response(PROVIDER, raw)
    return FilteredQueryResponse(
        metric=normalized["metric"],
        datapoints=normalized["datapoints"],
        matched_labels=[
            tag.split(":")[0] for tag in normalized.get("tags", []) if ":" in tag
        ],
    )


if __name__ == "__main__":
    # Example usage (remove or adapt when integrating into a real service)
    req = FilteredQueryRequest(
        metric="system.cpu.idle",
        filter_expr="env=prod and host:web01",
        start="now-10m",
        end="now",
    )
    result = filter_metric_dimensions(req)
    print(result)
