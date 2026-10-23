import os
from typing import Any, Dict

from document_models import TextExtractionResult

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620")


def extract_document_fields(text_result: TextExtractionResult) -> Dict[str, Any]:
    from anthropic import Anthropic

    if not ANTHROPIC_API_KEY:
        raise RuntimeError("Anthropic API key is required")
    client = Anthropic()
    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=512,
        messages=[
            {"role": "user", "content": f"Extract structured fields as JSON from this OCR text:\n{text_result.text}"},
        ],
    )
    return {"model": ANTHROPIC_MODEL, "content": getattr(message, "content", [])}
