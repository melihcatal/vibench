import os
from typing import List, Dict, Any, Optional
from mindee import Client, documents
from mindee.documents import CustomV1
from document_models import KeyValuePair, KeyValueExtractionResponse


def extract_key_values(
    image_path: str, mime_type: Optional[str] = None
) -> KeyValueExtractionResponse:
    """
    Extract key-value pairs from a form-like document using Mindee.
    """
    mindee_api_key = os.environ.get("MINDEE_API_KEY")
    if not mindee_api_key:
        raise ValueError("MINDEE_API_KEY environment variable is required")

    mindee_client = Client(api_key=mindee_api_key)

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with open(image_path, "rb") as f:
        input_doc = mindee_client.source_from_file(f)

    result = mindee_client.parse(
        documents.TypeCustomV1, input_doc, endpoint_name="form_extractor"
    )

    key_value_pairs = []

    for field_name, field in result.document.fields.items():
        if field.value:
            key_value_pair = KeyValuePair(
                key=field_name,
                value=str(field.value),
                confidence=field.confidence,
                bounding_box=field.bounding_box.to_dict()
                if hasattr(field, "bounding_box")
                else None,
            )
            key_value_pairs.append(key_value_pair)

    return KeyValueExtractionResponse(
        key_values=key_value_pairs,
        raw_response=result.document.to_dict(),
        provider="mindee",
    )
