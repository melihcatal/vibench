from __future__ import annotations

import json

from model_client import build_client
from model_models import ExtractionRequest


def extract_json(request: ExtractionRequest) -> dict:
    client = build_client()
    user_prompt = (
        "Extract structured data from the text below. Return only a valid JSON object "
        "that matches this schema hint as closely as possible.\n\n"
        f"SCHEMA_HINT:\n{json.dumps(request.schema_hint, ensure_ascii=False, indent=2)}\n\n"
        f"TEXT:\n{request.text}"
    )
    payload = client.responses_json(
        system_prompt=request.system_prompt,
        user_prompt=user_prompt,
        model=request.config.model,
    )
    return json.loads(payload)
