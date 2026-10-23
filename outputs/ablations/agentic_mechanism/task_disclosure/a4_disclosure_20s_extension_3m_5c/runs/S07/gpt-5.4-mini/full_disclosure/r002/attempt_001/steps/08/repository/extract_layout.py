import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "gpt-5.4-mini"


def extract_layout(document_bytes: bytes, mime_type: str = "application/pdf", model: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    model_name = model or DEFAULT_MODEL
    payload = {
        "model": model_name,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Extract the document layout as structured JSON with blocks, lines, tables, and other layout elements.",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:{mime_type};base64,{document_bytes.decode('latin1')}"
                        if mime_type.startswith("image/")
                        else {"type": "input_text", "text": "Document bytes provided separately."},
                    },
                ],
            }
        ],
        "response_format": {"type": "json_object"},
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()
