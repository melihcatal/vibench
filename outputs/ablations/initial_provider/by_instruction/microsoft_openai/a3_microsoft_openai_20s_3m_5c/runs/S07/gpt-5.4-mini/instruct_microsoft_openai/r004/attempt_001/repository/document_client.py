import os
from typing import Any, Dict, Optional

from openai import OpenAI

from document_models import DocumentRequest, DocumentResponse, normalize_blocks, normalize_text


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _vision_prompt(task: str) -> str:
    return task.strip()


def process_document(request: DocumentRequest, task: str, model: Optional[str] = None) -> DocumentResponse:
    client = _client()
    response = client.responses.create(
        model=model or os.environ.get("OPENAI_VISION_MODEL", "gpt-4.1-mini"),
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": _vision_prompt(task)},
                    {"type": "input_image", "image_url": request.source},
                ],
            }
        ],
    )
    raw: Dict[str, Any] = response.model_dump() if hasattr(response, "model_dump") else dict(response)
    text = normalize_text(raw.get("output_text") or raw.get("text"))
    return DocumentResponse(text=text, blocks=normalize_blocks(raw), raw=raw)
