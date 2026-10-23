from __future__ import annotations

import json
from typing import Any, Dict

from model_client import complete_text
from model_models import InferenceRequest, strip_code_fences


def extract_json(text: str, schema_hint: str, model: str | None = None) -> Dict[str, Any]:
    request = InferenceRequest(
        system_prompt=(
            "You are an information extraction assistant. Return only valid JSON that matches the requested schema."
        ),
        user_prompt=(
            "Extract structured data from the input text.\n"
            f"Schema hint: {schema_hint}\n\n"
            f"Input text:\n{text}"
        ),
        temperature=0.0,
        max_tokens=500,
        model=model,
    )
    response = complete_text(request)
    payload = strip_code_fences(response.text)
    return json.loads(payload)
