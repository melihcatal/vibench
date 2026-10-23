from __future__ import annotations

import json

from model_client import choose_model, generate_text
from model_models import ChatTurn, build_json_extraction_prompt


def extract_json(text: str, schema_hint: str, model: str | None = None) -> dict:
    prompt = build_json_extraction_prompt(schema_hint=schema_hint, text=text)
    result = generate_text(
        [
            ChatTurn(
                role="system",
                content="Return only valid JSON with no markdown fences or extra commentary.",
            ),
            ChatTurn(role="user", content=prompt),
        ],
        model=choose_model("extract", model),
        temperature=0,
        max_output_tokens=500,
    )
    return {
        "provider": "openai",
        "model": result.model,
        "data": json.loads(result.text),
        "usage": result.usage,
    }
