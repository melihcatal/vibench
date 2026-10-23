from __future__ import annotations

import json

from model_client import choose_model, chat_completion
from model_models import JsonExtractionRequest, parse_json_object

PROVIDER = "openai"
PROVIDER_MODEL = "gpt-4o-mini"


def extract_json(text: str, schema_hint: str, model: str | None = None) -> str:
    req = JsonExtractionRequest(text=text, schema_hint=schema_hint, model=model)
    selected_model = choose_model("extract", req.model or PROVIDER_MODEL)
    content = chat_completion(
        selected_model,
        [
            {"role": "system", "content": "Extract structured JSON only. Return valid JSON with no markdown."},
            {"role": "user", "content": f"Schema hint: {req.schema_hint}\n\nText:\n{req.text}"},
        ],
        temperature=req.temperature,
        response_format={"type": "json_object"},
    )
    return json.dumps(parse_json_object(content), ensure_ascii=False)
