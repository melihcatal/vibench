import json
import os
from typing import Any, Dict

from observability_client import create_observability_client, load_observability_config


def metric_annotation_safety(text: str) -> Dict[str, Any]:
    cfg = load_observability_config()
    client = create_observability_client(cfg)
    response = client.responses.create(
        model=os.environ.get("AZURE_OPENAI_METRIC_MODEL", "gpt-5.4-mini"),
        input=[
            {"role": "system", "content": "Assess metric annotations for unsafe text and return JSON only."},
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(response.output_text or "{}")
