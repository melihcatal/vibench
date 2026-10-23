import os
from typing import List, Dict, Any
import base64
from google.cloud import documentai
from document_client import get_documentai_client
from document_models import KeyValueResponse, KeyValuePair, KeyValueExtractionRequest


def extract_key_values(request: KeyValueExtractionRequest) -> KeyValueResponse:
    """Extract key-value pairs from a form-like document using Google Cloud Document AI."""

    client = get_documentai_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")
    processor_id = os.getenv("DOCUMENT_AI_PROCESSOR_ID", "your-processor-id")

    if request.image_path:
        with open(request.image_path, "rb") as image_file:
            content = image_file.read()
    elif request.image_base64:
        content = base64.b64decode(request.image_base64)
    else:
        raise ValueError("Either image_path or image_base64 must be provided")

    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    raw_document = documentai.RawDocument(
        content=content, mime_type=request.mime_type or "image/jpeg"
    )

    request_docai = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request_docai)
    document = result.document

    key_value_pairs: List[KeyValuePair] = []

    if hasattr(document, "entities"):
        for entity in document.entities:
            key_text = ""
            value_text = ""
            confidence = entity.confidence if hasattr(entity, "confidence") else 0.0

            if entity.type_ == "key":
                key_text = extract_entity_text(document.text, entity)
            elif entity.type_ == "value":
                value_text = extract_entity_text(document.text, entity)
            elif hasattr(entity, "properties"):
                for prop in entity.properties:
                    if prop.type_ == "key":
                        key_text = extract_entity_text(document.text, prop)
                    elif prop.type_ == "value":
                        value_text = extract_entity_text(document.text, prop)

            if key_text or value_text:
                key_value_pairs.append(
                    KeyValuePair(key=key_text, value=value_text, confidence=confidence)
                )

    return KeyValueResponse(
        pairs=key_value_pairs,
        provider="google_document_ai",
        model="form_parser",
        raw_response=result,
    )


def extract_entity_text(full_text: str, entity) -> str:
    """Extract text from an entity in Document AI response."""
    if not hasattr(entity, "text_anchor") or not entity.text_anchor:
        return ""

    text_anchor = entity.text_anchor
    if not text_anchor.text_segments:
        return ""

    text_segment = text_anchor.text_segments[0]
    start_index = text_segment.start_index
    end_index = text_segment.end_index
    return full_text[start_index:end_index]
