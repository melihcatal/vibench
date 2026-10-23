from datetime import datetime
from typing import Any, Dict, Mapping

from observability_client import get_json
from observability_models import isoformat


def compare_metric_series(
    metric_name: str,
    start: datetime,
    end: datetime,
    left: Mapping[str, str],
    right: Mapping[str, str],
) -> Dict[str, Any]:
    left_query = ",".join(f"{k}:{v}" for k, v in left.items()) or "*"
    right_query = ",".join(f"{k}:{v}" for k, v in right.items()) or "*"
    return {
        "left": get_json(
            "/api/v1/query",
            params={
                "from": isoformat(start),
                "to": isoformat(end),
                "query": f"avg:{metric_name}{{{left_query}}}",
            },
        ),
        "right": get_json(
            "/api/v1/query",
            params={
                "from": isoformat(start),
                "to": isoformat(end),
                "query": f"avg:{metric_name}{{{right_query}}}",
            },
        ),
    }
