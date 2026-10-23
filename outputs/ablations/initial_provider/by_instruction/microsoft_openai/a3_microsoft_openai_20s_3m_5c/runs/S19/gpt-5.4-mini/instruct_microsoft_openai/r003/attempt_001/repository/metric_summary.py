import json
import os
from typing import Any, Dict

from observability_client import create_observability_client, load_observability_config


def metric_summary(start_time: str, end_time: str) -> Dict[str, Any]:
    cfg = load_observability_config()
    client = create_observability_client(cfg)
    response = client.responses.create(
        model=os.environ.get("AZURE_OPENAI_METRIC_MODEL", "gpt-5.4-mini"),
        input=[
            {"role": "system", "content": "Summarize recent managed metric trends and anomalies as JSON."},
            {"role": "user", "content": f"Summarize metric activity between {start_time} and {end_time}."},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(response.output_text or "{}")
