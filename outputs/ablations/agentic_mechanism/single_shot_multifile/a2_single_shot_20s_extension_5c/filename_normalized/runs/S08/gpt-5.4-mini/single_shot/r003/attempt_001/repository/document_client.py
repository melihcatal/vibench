import json
import os
from dataclasses import dataclass
from typing import Any

from google import genai


@dataclass
class DocumentClientConfig:
    api_key: str | None = None
    model: str = "gemini-1.5-pro"


def load_document_client_config() -> DocumentClientConfig:
    return DocumentClientConfig(api_key=os.getenv("GOOGLE_API_KEY"), model=os.getenv("DOCUMENT_EXTRACT_MODEL", "gemini-1.5-pro"))


def create_document_ai_client() -> genai.Client:
    config = load_document_client_config()
    if not config.api_key:
        raise ValueError("GOOGLE_API_KEY is required for Google Gemini document extraction")
    return genai.Client(api_key=config.api_key)


def extract_structured_fields(client: genai.Client, request: Any, model: str | None = None) -> dict:
    active_model = model or load_document_client_config().model
    prompt = json.dumps({"document_type": request.document_type, "document_id": request.document_id, "text": request.text, "output_schema": request.schema_hint()}, ensure_ascii=False)
    response = client.models.generate_content(model=active_model, contents=prompt)
    text = getattr(response, "text", None) or str(response)
    try:
        return json.loads(text)
    except Exception:
        return {"raw_text": text, "document_type": request.document_type, "document_id": request.document_id}
