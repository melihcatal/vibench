from __future__ import annotations

import json

from model_client import get_client, load_config, choose_model
from model_models import PromptRequest, response_to_normalized

SYSTEM_PROMPT = "Extract structured JSON from the user's text. Return only valid JSON."


def extract_json(text: str) -> dict:
    config = load_config()
    client = get_client(config)
    model = choose_model("extract", config)
    request = PromptRequest(text=text, system=SYSTEM_PROMPT)
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": request.system},
            {"role": "user", "content": request.text},
        ],
        response_format={"type": "json_object"},
    )
    normalized = response_to_normalized(response, model).text
    return json.loads(normalized)
