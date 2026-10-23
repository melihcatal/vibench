from datetime import datetime
from typing import Any, Dict

from observability_client import get_json
from observability_models import isoformat


def query_metric_window(
    metric_name: str, start: datetime, end: datetime
) -> Dict[str, Any]:
    return get_json(
        "/api/v1/query",
        params={
            "from": isoformat(start),
            "to": isoformat(end),
            "query": f"avg:{metric_name}{{*}}",
        },
    )
