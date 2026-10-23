from __future__ import annotations

import json
import os
from typing import Any, Dict

import requests


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def extract_document_fields(
    normalized_text: str, schema: Dict[str, str]
) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    prompt = {
        "schema": schema,
        "document_text": normalized_text,
        "instructions": "Extract the requested fields and return strict JSON with null for missing values.",
    }
    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "input": [
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": json.dumps(prompt)}],
                }
            ],
        },
        timeout=90,
    )
    response.raise_for_status()
    output_text = response.json()["output"][0]["content"][0]["text"]
    return json.loads(output_text)
