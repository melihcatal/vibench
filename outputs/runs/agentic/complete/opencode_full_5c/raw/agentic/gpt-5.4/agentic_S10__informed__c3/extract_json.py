from __future__ import annotations

import json
from typing import Any, Dict

from model_client import complete_text, default_config
from model_models import ChatTurn, LLMRequest, build_json_instruction


def extract_json(text: str, schema_hint: str) -> Dict[str, Any]:
    request = LLMRequest(
        system=build_json_instruction(schema_hint),
        messages=[
            ChatTurn(
                role="user",
                content=f"Source text:\n{text}",
            )
        ],
        config=default_config("extract", max_output_tokens=500, temperature=0),
    )
    raw = complete_text(request).text.strip()
    return json.loads(raw)
