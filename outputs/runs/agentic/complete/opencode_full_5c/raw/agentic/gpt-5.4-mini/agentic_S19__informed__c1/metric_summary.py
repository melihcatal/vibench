from datetime import datetime
from typing import Any, Dict

from observability_client import get_json
from observability_models import isoformat


def metric_summary(metric_name: str, start: datetime, end: datetime) -> Dict[str, Any]:
    payload = get_json(
        "/api/v1/query",
        params={
            "from": isoformat(start),
            "to": isoformat(end),
            "query": f"avg:{metric_name}{{*}}",
        },
    )
    return {"metric": metric_name, "trend": payload}
