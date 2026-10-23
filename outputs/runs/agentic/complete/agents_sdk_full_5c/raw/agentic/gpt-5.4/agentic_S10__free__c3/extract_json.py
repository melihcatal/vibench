from __future__ import annotations

import json
from typing import Any, Dict

from model_client import get_openai_client, pick_chat_model
from model_models import ChatRequest, extract_text_from_response


def extract_json(text: str, schema_hint: str) -> Dict[str, Any]:
    client = get_openai_client()
    request = ChatRequest(
        system_prompt=(
            "Extract structured data from unstructured text. "
            "Return only valid JSON matching the requested schema hint."
        ),
        user_prompt=f"Schema hint:\n{schema_hint}\n\nText:\n{text}",
        model=pick_chat_model("extract"),
        temperature=0.0,
        max_output_tokens=400,
    )
    response = client.chat.completions.create(
        model=request.model,
        messages=request.to_openai_messages(),
        temperature=request.temperature,
        max_tokens=request.max_output_tokens,
        response_format={"type": "json_object"},
    )
    content = extract_text_from_response(response)
    return json.loads(content)
