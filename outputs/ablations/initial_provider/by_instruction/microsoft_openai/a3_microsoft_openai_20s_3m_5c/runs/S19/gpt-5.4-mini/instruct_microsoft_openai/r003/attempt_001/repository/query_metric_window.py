import os
from typing import Any, Dict, Optional

from observability_client import create_observability_client, load_observability_config
from observability_models import MetricQuery, normalize_series


def query_metric_window(start_time: str, end_time: str, metric_name: Optional[str] = None, resource_id: Optional[str] = None) -> Dict[str, Any]:
    cfg = load_observability_config({"metric_name": metric_name, "resource_id": resource_id})
    client = create_observability_client(cfg)
    query = MetricQuery(cfg.metric_namespace, cfg.metric_name, start_time, end_time, resource_id=cfg.resource_id)
    response = client.responses.create(
        model=os.environ.get("AZURE_OPENAI_METRIC_MODEL", "gpt-5.4-mini"),
        input=[
            {
                "role": "system",
                "content": "You query Microsoft Azure Monitor style managed metrics and return structured JSON only.",
            },
            {
                "role": "user",
                "content": f"Query metric {query.metric_namespace}/{query.metric_name} from {query.start_time} to {query.end_time} for resource {query.resource_id or 'all'}.",
            },
        ],
        response_format={"type": "json_object"},
    )
    payload = response.output_text or "{}"
    import json

    return normalize_series(json.loads(payload)).__dict__
