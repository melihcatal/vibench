from typing import Dict, List, Optional
import os
from google.cloud import documentai_v1 as documentai
from document_client import get_document_processor_client
from document_models import KeyValueResponse


def extract_key_values(
    image_path: str, processor_id: Optional[str] = None
) -> KeyValueResponse:
    """Extract key-value pairs from a form-like document using Google Cloud Document AI."""
    client = get_document_processor_client()
    processor_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}/locations/us/processors/{processor_id or os.getenv('GOOGLE_DOCUMENT_AI_PROCESSOR_ID')}"

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    request = {
        "name": processor_name,
        "raw_document": {
            "content": content,
            "mime_type": "application/pdf"
            if image_path.endswith(".pdf")
            else "image/png",
        },
    }

    result = client.process_document(request=request)
    document = result.document

    key_values = []
    for entity in document.entities:
        if entity.type_ == "key_value_pair":
            key = None
            value = None
            for property_ in entity.properties:
                if property_.type_ == "key":
                    key = property_.mention_text
                elif property_.type_ == "value":
                    value = property_.mention_text

            if key and value:
                key_values.append(
                    {
                        "key": key,
                        "value": value,
                        "key_bounding_box": {
                            "vertices": [
                                {"x": vertex.x, "y": vertex.y}
                                for vertex in entity.page_anchor.page_refs[
                                    0
                                ].bounding_poly.vertices
                            ]
                        }
                        if entity.page_anchor.page_refs
                        else None,
                        "value_bounding_box": {
                            "vertices": [
                                {"x": vertex.x, "y": vertex.y}
                                for vertex in property_.page_anchor.page_refs[
                                    0
                                ].bounding_poly.vertices
                            ]
                        }
                        if property_.page_anchor.page_refs
                        else None,
                    }
                )

    return KeyValueResponse(key_values=key_values)
