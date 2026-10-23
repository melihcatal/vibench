import json
import os
from typing import Any, Dict

from observability_client import create_observability_client, load_observability_config


def metrics_export_archive(snapshot_uri: str) -> Dict[str, Any]:
    cfg = load_observability_config()
    client = create_observability_client(cfg)
    response = client.responses.create(
        model=os.environ.get("AZURE_OPENAI_METRIC_MODEL", "gpt-5.4-mini"),
        input=[
            {"role": "system", "content": "Prepare managed metric export archival metadata in JSON."},
            {"role": "user", "content": f"Archive exported metric snapshot from {snapshot_uri}."},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(response.output_text or "{}")
