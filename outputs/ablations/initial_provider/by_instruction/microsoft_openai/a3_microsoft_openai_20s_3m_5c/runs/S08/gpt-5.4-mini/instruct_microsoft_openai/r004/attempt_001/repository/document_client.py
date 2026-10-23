import json
import os
from typing import Any, Dict

from openai import OpenAI

from document_models import StructuredDocumentRequest, StructuredDocumentResponse


def load_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_structured_document(request: StructuredDocumentRequest) -> StructuredDocumentResponse:
    client = load_client()
    prompt = json.dumps({"schema_name": request.schema_name, "schema": request.schema})
    messages = [
        {"role": "system", "content": "Extract structured data strictly as JSON."},
        {"role": "user", "content": prompt},
    ]
    response = client.responses.create(model=request.model, input=messages)
    text = response.output_text
    content: Dict[str, Any]
    try:
        content = json.loads(text)
    except Exception:
        content = {"text": text}
    return StructuredDocumentResponse(provider="openai", model=request.model, content=content, raw={"response_id": response.id})
