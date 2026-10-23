from __future__ import annotations

import json
from typing import Any, Dict

from model_client import HostedModelClient


def extract_json(text: str, schema_hint: str = "Return keys: people, organizations, dates, locations, summary") -> Dict[str, Any]:
    client = HostedModelClient()
    request = client.build_request(
        task="json",
        system_prompt=(
            "You extract structured data as valid JSON only. "
            "Do not wrap the JSON in markdown fences or extra commentary."
        ),
        user_prompt=f"Schema hint: {schema_hint}\n\nSource text:\n{text}",
        temperature=0.0,
        max_tokens=400,
    )
    result = client.generate(request)
    return json.loads(result.text)
