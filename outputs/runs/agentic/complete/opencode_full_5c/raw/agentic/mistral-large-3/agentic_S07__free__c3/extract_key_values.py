from typing import Dict, List, Optional
import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from document_client import get_google_vision_client
from document_models import KeyValueResponse


def extract_key_values(image_path: str) -> KeyValueResponse:
    """Extract key-value pairs from a form-like document using Google Cloud Vision."""
    client = get_google_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision_v1.types.Image(content=content)
    features = [{"type_": vision_v1.Feature.Type.DOCUMENT_TEXT_DETECTION}]

    request = vision_v1.types.AnnotateImageRequest(image=image, features=features)
    response = client.annotate_image(request)

    if response.error.message:
        raise ValueError(f"Google Cloud Vision API error: {response.error.message}")

    key_values = []
    for form_field in response.form_field_annotation:
        field_name = form_field.field_name.text if form_field.field_name else ""
        field_value = form_field.field_value.text if form_field.field_value else ""

        key_bounding_box = (
            {
                "vertices": [
                    {"x": vertex.x, "y": vertex.y}
                    for vertex in form_field.field_name.bounding_box.vertices
                ]
            }
            if form_field.field_name
            else None
        )

        value_bounding_box = (
            {
                "vertices": [
                    {"x": vertex.x, "y": vertex.y}
                    for vertex in form_field.field_value.bounding_box.vertices
                ]
            }
            if form_field.field_value
            else None
        )

        key_values.append(
            {
                "key": field_name,
                "value": field_value,
                "key_bounding_box": key_bounding_box,
                "value_bounding_box": value_bounding_box,
                "confidence": form_field.confidence,
            }
        )

    return KeyValueResponse(
        key_values=key_values, provider="google_vision", model="document_text_detection"
    )
