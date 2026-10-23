import json
import os
from typing import Any, Dict, Optional

from openai import OpenAI


def get_api_key() -> Optional[str]:
    return os.getenv("OPENAI_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")


def get_model_name() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def get_client() -> OpenAI:
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=get_api_key(), base_url=base_url)
    return OpenAI(api_key=get_api_key())


def chat_json(prompt: str, schema_hint: Dict[str, Any]) -> Dict[str, Any]:
    client = get_client()
    response = client.responses.create(
        model=get_model_name(),
        input=[
            {
                "role": "system",
                "content": "You extract structured document fields as JSON."
            },
            {
                "role": "user",
                "content": f"{prompt}\n\nReturn JSON matching: {json.dumps(schema_hint, ensure_ascii=False)}"
            },
        ],
    )
    text = getattr(response, "output_text", "") or "{}"
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"text": text}
