import os
from typing import Dict, Any, List
from document_client import DocumentAICLient
from document_models import DocumentExtractionRequest, KeyValueExtractionResponse
from google.cloud import documentai_v1 as documentai

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
# For key-value pair extraction, a specialized form parser processor is often used.
# Replace with your specific form parser processor ID.
FORM_PARSER_PROCESSOR_ID = os.getenv(
    "GOOGLE_DOCUMENT_AI_FORM_PARSER_PROCESSOR_ID", "your-form-parser-processor-id"
)


def extract_key_values_from_document(
    request: DocumentExtractionRequest,
) -> KeyValueExtractionResponse:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    if not FORM_PARSER_PROCESSOR_ID:
        raise ValueError(
            "GOOGLE_DOCUMENT_AI_FORM_PARSER_PROCESSOR_ID environment variable not set."
        )

    document_ai_client = DocumentAICLient(location=request.location)
    document = document_ai_client.process_document(
        project_id=PROJECT_ID,
        processor_id=request.processor_id
        if request.processor_id != ""
        else FORM_PARSER_PROCESSOR_ID,
        content=request.content,
        mime_type=request.mime_type,
    )

    key_value_pairs = []
    for entity in document.entities:
        if (
            entity.type == "form_field"
        ):  # This might vary based on the processor and document type
            key = entity.mention_text if entity.mention_text else ""
            value = ""
            if entity.page_anchor.page_refs:
                # This is a simplified way to get value, actual implementation might need more logic
                # For more robust value extraction, you might need to iterate through properties or linked entities
                pass  # No direct value extraction here, assuming it's part of the entity structure

            # For Google Document AI, form fields are usually represented as entities.
            # The value might be in a separate child entity or within the properties of the parent entity.
            # This example assumes a simple key-value structure directly from entities for demonstration.
            if (
                hasattr(entity, "properties") and entity.properties
            ):  # Check for properties attribute and if it's not empty
                for prop in entity.properties:
                    if (
                        prop.type == "value" and prop.mention_text
                    ):  # Assuming a property type 'value'
                        value = prop.mention_text
                        break
            elif (
                entity.normalized_value.text_segments
            ):  # Try to get value from normalized_value if properties not available
                value = entity.normalized_value.text_segments[0].text_segment.text
            elif (
                entity.text_anchor.text_segments
            ):  # Fallback to text_anchor if no other value found
                value = entity.text_anchor.text_segments[0].text_segment.text

            key_value_pairs.append(
                {"key": key, "value": value, "confidence": entity.confidence}
            )

    return KeyValueExtractionResponse(key_value_pairs=key_value_pairs)
