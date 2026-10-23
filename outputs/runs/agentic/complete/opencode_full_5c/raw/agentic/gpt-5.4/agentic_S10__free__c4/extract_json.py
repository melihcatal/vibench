from __future__ import annotations

import json

from model_client import create_text_response
from model_models import ExtractionRequest, normalize_text_response, trim_text


def extract_json(
    source_text: str,
    schema_hint: dict,
    instruction: str = "Extract the requested fields as strict JSON.",
    model: str | None = None,
) -> dict:
    request = ExtractionRequest(
        instruction=instruction,
        source_text=source_text,
        schema_hint=schema_hint,
        model=model,
    )
    user_prompt = (
        f"{request.instruction}\n"
        f"Return valid JSON only with no markdown fences.\n"
        f"Schema hint:\n{json.dumps(request.schema_hint, ensure_ascii=False)}\n\n"
        f"Source text:\n{trim_text(request.source_text, 16000)}"
    )
    response = create_text_response(
        system_prompt="You extract structured information from text and return strict JSON output.",
        user_prompt=user_prompt,
        task_name="extraction",
        model=request.model,
        temperature=request.temperature,
        max_output_tokens=request.max_output_tokens,
    )
    normalized = normalize_text_response(response)
    parsed = json.loads(normalized.text)
    return {"data": parsed, "model": normalized.model, "usage": normalized.usage}
