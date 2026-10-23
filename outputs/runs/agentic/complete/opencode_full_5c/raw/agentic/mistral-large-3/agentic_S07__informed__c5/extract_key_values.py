import os
from typing import List
from mindee import Client, documents
from mindee.input import LocalInputSource
from .document_models import KeyValuePair, OCRTextBlock


def extract_key_values_from_image(file_path: str) -> List[KeyValuePair]:
    """
    Extracts key-value pairs from a form-like document using Mindee OCR.
    Requires MINDEE_API_KEY environment variable.
    """
    api_key = os.getenv("MINDEE_API_KEY")
    if not api_key:
        raise ValueError("MINDEE_API_KEY environment variable not set")

    client = Client(api_key=api_key)
    input_source = LocalInputSource(file_path)
    response = client.parse(
        document_type=documents.TypeDocumentFile, input_source=input_source
    )

    key_values = []
    for page in response.document.inference.pages:
        for field in page.fields:
            key_block = OCRTextBlock(
                text=field.label.value if field.label else "",
                bounding_box={
                    "x1": field.label.bounding_box[0][0] if field.label else 0,
                    "y1": field.label.bounding_box[0][1] if field.label else 0,
                    "x2": field.label.bounding_box[2][0] if field.label else 0,
                    "y2": field.label.bounding_box[2][1] if field.label else 0,
                }
                if field.label
                else {"x1": 0, "y1": 0, "x2": 0, "y2": 0},
                confidence=field.label.confidence if field.label else 0,
            )

            value_block = OCRTextBlock(
                text=field.value.value if field.value else "",
                bounding_box={
                    "x1": field.value.bounding_box[0][0] if field.value else 0,
                    "y1": field.value.bounding_box[0][1] if field.value else 0,
                    "x2": field.value.bounding_box[2][0] if field.value else 0,
                    "y2": field.value.bounding_box[2][1] if field.value else 0,
                }
                if field.value
                else {"x1": 0, "y1": 0, "x2": 0, "y2": 0},
                confidence=field.value.confidence if field.value else 0,
            )

            key_values.append(
                KeyValuePair(
                    key=key_block, value=value_block, confidence=field.confidence
                )
            )

    return key_values
