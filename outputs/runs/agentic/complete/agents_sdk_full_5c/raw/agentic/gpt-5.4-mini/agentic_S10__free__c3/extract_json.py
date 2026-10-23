from __future__ import annotations

import json
from typing import Any, Dict, Optional

from openai import OpenAI

from model_client import build_client, model_for_task
from model_models import ChatRequest


OPENAI_JSON_MODEL = "gpt-4.1-mini"


def extract_json(text: str, schema_hint: str, client: Optional[OpenAI] = None) -> Dict[str, Any]:
    client = client or build_client()
    request = ChatRequest(
        task="extract_json",
        model=model_for_task("extract_json", default=OPENAI_JSON_MODEL),
        system_prompt="You extract structured JSON only, with no commentary.",
        user_prompt=f"Extract JSON from this text using the following schema hint:\n{schema_hint}\n\nText:\n{text}",
    )
    response = client.chat.completions.create(
        model=request.model,
        messages=request.messages(),
        temperature=0,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or "{}"
    return json.loads(content)
