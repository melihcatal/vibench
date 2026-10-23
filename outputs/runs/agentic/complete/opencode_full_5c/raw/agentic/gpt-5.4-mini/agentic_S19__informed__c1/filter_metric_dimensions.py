from datetime import datetime
from typing import Any, Dict, Mapping

from observability_client import get_json
from observability_models import isoformat


def filter_metric_dimensions(
    metric_name: str, start: datetime, end: datetime, dimensions: Mapping[str, str]
) -> Dict[str, Any]:
    dim_query = ",".join(f"{k}:{v}" for k, v in dimensions.items()) or "*"
    return get_json(
        "/api/v1/query",
        params={
            "from": isoformat(start),
            "to": isoformat(end),
            "query": f"avg:{metric_name}{{{dim_query}}}",
        },
    )
