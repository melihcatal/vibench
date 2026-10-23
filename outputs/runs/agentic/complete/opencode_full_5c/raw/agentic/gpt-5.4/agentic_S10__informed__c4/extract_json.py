from __future__ import annotations

import json

from model_client import choose_chat_model, get_openai_client
from model_models import compact_json_schema


def extract_json(text: str) -> dict:
    client = get_openai_client()
    response = client.responses.create(
        model=choose_chat_model("extract"),
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Extract structured information from the provided text.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": text}],
            },
        ],
        text=compact_json_schema(),
    )
    return json.loads(response.output_text)
