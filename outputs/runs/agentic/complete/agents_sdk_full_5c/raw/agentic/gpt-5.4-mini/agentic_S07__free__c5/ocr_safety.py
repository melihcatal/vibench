import os
from typing import Any, Dict

from document_models import TextExtractionResult

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def check_ocr_text_safety(text_result: TextExtractionResult) -> Dict[str, Any]:
    from openai import OpenAI

    if not OPENAI_API_KEY:
        raise RuntimeError("OpenAI API key is required")
    client = OpenAI()
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "Classify document text for unsafe content and return a concise JSON verdict.",
            },
            {"role": "user", "content": text_result.text},
        ],
    )
    return {"model": OPENAI_MODEL, "response_id": response.id, "output_text": response.output_text}
