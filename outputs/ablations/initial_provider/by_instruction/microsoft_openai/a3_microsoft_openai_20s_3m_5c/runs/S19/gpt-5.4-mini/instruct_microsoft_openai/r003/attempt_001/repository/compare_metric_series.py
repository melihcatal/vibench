import json
import os
from typing import Any, Dict, Optional

from observability_client import create_observability_client, load_observability_config


def compare_metric_series(start_time: str, end_time: str, left_filter: str, right_filter: str, metric_name: Optional[str] = None) -> Dict[str, Any]:
    cfg = load_observability_config({"metric_name": metric_name})
    client = create_observability_client(cfg)
    response = client.responses.create(
        model=os.environ.get("AZURE_OPENAI_METRIC_MODEL", "gpt-5.4-mini"),
        input=[
            {"role": "system", "content": "Compare two Azure managed metric series and return JSON only."},
            {"role": "user", "content": f"Compare {cfg.metric_namespace}/{cfg.metric_name} from {start_time} to {end_time} for {left_filter} versus {right_filter}."},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(response.output_text or "{}")
