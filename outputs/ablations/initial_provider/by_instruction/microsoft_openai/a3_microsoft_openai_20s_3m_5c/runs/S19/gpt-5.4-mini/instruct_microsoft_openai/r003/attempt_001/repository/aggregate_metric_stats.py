import json
import os
from typing import Any, Dict, Optional

from observability_client import create_observability_client, load_observability_config
from observability_models import MetricQuery


def aggregate_metric_stats(start_time: str, end_time: str, aggregation: str, metric_name: Optional[str] = None) -> Dict[str, Any]:
    cfg = load_observability_config({"metric_name": metric_name})
    client = create_observability_client(cfg)
    query = MetricQuery(cfg.metric_namespace, cfg.metric_name, start_time, end_time, aggregation=aggregation)
    response = client.responses.create(
        model=os.environ.get("AZURE_OPENAI_METRIC_MODEL", "gpt-5.4-mini"),
        input=[
            {"role": "system", "content": "Summarize managed metric aggregates in JSON."},
            {"role": "user", "content": f"Aggregate {query.metric_namespace}/{query.metric_name} using {query.aggregation} between {start_time} and {end_time}."},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(response.output_text or "{}")
