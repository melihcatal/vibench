from __future__ import annotations

from model_client import get_model_name, get_openai_client
from model_models import parse_json_response

PROVIDER = "openai"
MODEL_FAMILY = "gpt-4o"


def extract_json(text: str, schema_hint: str, model: str | None = None) -> dict:
    client = get_openai_client()
    response = client.responses.create(
        model=get_model_name(model),
        input=[
            {
                "role": "system",
                "content": (
                    "Extract structured JSON from the input. Return only valid JSON with fields aligned to the schema hint."
                ),
            },
            {"role": "user", "content": f"Schema hint:\n{schema_hint}\n\nText:\n{text}"},
        ],
    )
    return parse_json_response(response.output_text)
