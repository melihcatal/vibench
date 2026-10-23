import os
from typing import List, Dict, Any
import requests
from document_client import get_google_document_ai_client
from document_models import (
    KeyValueExtractionRequest,
    KeyValueExtractionResponse,
    KeyValuePair,
)


def extract_key_values(
    image_path: str, processor_id: str = None
) -> KeyValueExtractionResponse:
    """
    Extract key-value pairs from a form-like document using Google Document AI.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us")

    if not processor_id:
        processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")

    if not project_id or not processor_id:
        raise ValueError("Google Document AI credentials not configured")

    with open(image_path, "rb") as image_file:
        image_content = image_file.read()

    from google.cloud import documentai_v1 as documentai
    from google.api_core.client_options import ClientOptions

    client_options = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=client_options)

    name = client.processor_path(project_id, location, processor_id)

    raw_document = documentai.RawDocument(content=image_content, mime_type="image/jpeg")

    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)

    key_values = []
    for entity in result.document.entities:
        key_value = KeyValuePair(
            key=entity.type_,
            value=entity.mention_text,
            confidence=entity.confidence,
            normalized_value=entity.normalized_value.text
            if entity.normalized_value
            else None,
        )
        key_values.append(key_value)

    return KeyValueExtractionResponse(
        key_values=key_values, provider="google_document_ai", raw_response=result
    )
