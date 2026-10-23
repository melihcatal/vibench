import json
import os
from typing import Any, Dict, Optional

from observability_client import create_observability_client, load_observability_config


def filter_metric_dimensions(start_time: str, end_time: str, dimension_filter: str, metric_name: Optional[str] = None) -> Dict[str, Any]:
    cfg = load_observability_config({"metric_name": metric_name})
    client = create_observability_client(cfg)
    response = client.responses.create(
        model=os.environ.get("AZURE_OPENAI_METRIC_MODEL", "gpt-5.4-mini"),
        input=[
            {"role": "system", "content": "Filter Azure managed metric series by dimensions and return JSON only."},
            {"role": "user", "content": f"Filter {cfg.metric_namespace}/{cfg.metric_name} between {start_time} and {end_time} where {dimension_filter}."},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(response.output_text or "{}")
