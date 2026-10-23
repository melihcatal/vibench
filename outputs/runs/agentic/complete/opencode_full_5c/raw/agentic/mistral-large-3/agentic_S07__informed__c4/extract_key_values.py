from google.cloud import documentai_v1 as documentai
import os
from typing import List, Dict, Any
from document_client import get_document_client
from document_models import KeyValuePair, KeyValueResponse


def extract_key_values_from_image(
    image_path: str, mime_type: str = "image/png"
) -> KeyValueResponse:
    """
    Extracts key-value pairs from a form-like document using Google Document AI.

    Args:
        image_path: Path to the document image file.
        mime_type: MIME type of the image (e.g., "image/png", "image/jpeg").

    Returns:
        KeyValueResponse containing extracted key-value pairs and metadata.
    """
    client = get_document_client("google")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = os.getenv("GOOGLE_DOCUMENT_AI_LOCATION", "us")
    processor_id = os.getenv("GOOGLE_DOCUMENT_AI_PROCESSOR_ID")

    if not all([project_id, processor_id]):
        raise ValueError(
            "Google Cloud project ID and processor ID must be set in environment variables."
        )

    processor_name = (
        f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    )

    with open(image_path, "rb") as image_file:
        image_content = image_file.read()

    request = {
        "name": processor_name,
        "raw_document": {"content": image_content, "mime_type": mime_type},
    }

    result = client.process_document(request=request)
    document = result.document

    key_value_pairs = []
    for page in document.pages:
        for form_field in page.form_fields:
            key = (
                form_field.field_name.text_anchor.content
                if form_field.field_name.text_anchor
                else ""
            )
            value = (
                form_field.field_value.text_anchor.content
                if form_field.field_value.text_anchor
                else ""
            )

            key_value_pairs.append(
                KeyValuePair(
                    key=key,
                    value=value,
                    key_bounding_box={
                        "vertices": [
                            {"x": vertex.x, "y": vertex.y}
                            for vertex in form_field.field_name.bounding_poly.normalized_vertices
                        ]
                    },
                    value_bounding_box={
                        "vertices": [
                            {"x": vertex.x, "y": vertex.y}
                            for vertex in form_field.field_value.bounding_poly.normalized_vertices
                        ]
                    },
                    confidence=form_field.field_name.confidence,
                )
            )

    return KeyValueResponse(
        key_value_pairs=key_value_pairs,
        pages=len(document.pages),
        provider="google_document_ai",
        model="pretrained-form-v2.0-2023-06-02",
    )
