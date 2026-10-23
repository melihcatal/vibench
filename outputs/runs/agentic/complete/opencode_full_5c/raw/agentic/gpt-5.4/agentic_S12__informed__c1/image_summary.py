from __future__ import annotations

import json
from typing import Any, Dict

from vision_client import OPENAI_PROVIDER, OPENAI_TEXT_MODEL, get_openai_client


def image_summary(
    labels_result: Dict[str, Any],
    description_result: Dict[str, Any],
    text_result: Dict[str, Any],
    safety_result: Dict[str, Any],
) -> dict:
    client = get_openai_client()
    prompt = {
        "labels": labels_result,
        "description": description_result,
        "text": text_result,
        "safety": safety_result,
    }
    response = client.responses.create(
        model=OPENAI_TEXT_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Create a concise summary of this visual analysis as JSON with keys summary, notable_text, and risk_notes. Data: "
                        + json.dumps(prompt),
                    }
                ],
            }
        ],
    )
    return {
        "provider": OPENAI_PROVIDER,
        "model": OPENAI_TEXT_MODEL,
        "summary": response.output_text.strip(),
    }
