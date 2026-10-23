from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI

from model_client import build_openai_client, resolve_structured_model
from model_models import normalize_json_response


SYSTEM_PROMPT = "Extract the requested fields and return only valid JSON."


def extract_json(text: str, *, schema_hint: str | None = None, client: OpenAI | None = None, model: str | None = None) -> dict[str, Any]:
    api_client = client or build_openai_client()
    model_name = model or resolve_structured_model()
    response = api_client.responses.create(
        model=model_name,
        instructions=SYSTEM_PROMPT + (f" Schema hint: {schema_hint}" if schema_hint else ""),
        input=text,
        response_format={"type": "json_object"},
    )
    return normalize_json_response(response)


if __name__ == "__main__":
    sample = os.environ.get("JSON_TEXT", "")
    if sample:
        print(json.dumps(extract_json(sample), ensure_ascii=False))
