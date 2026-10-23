from typing import List
from google.cloud import vision
from document_client import get_vision_client
from document_models import KeyValuePair


def extract_key_values_from_image(image_path: str) -> List[KeyValuePair]:
    """
    Extracts key-value pairs from a form-like document image using Google Cloud Vision API.
    """
    client = get_vision_client()
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    key_value_pairs = []
    # This is a simplified parsing logic. Real form parsing might require more complex logic.
    # Google's Vision API does not directly provide a key-value pair structure.
    # One would typically use Google Cloud Document AI for robust form parsing.
    # Here, we simulate by looking for text with a colon.

    texts = response.text_annotations
    if texts:
        full_text = texts[0].description
        for line in full_text.split("\n"):
            if ":" in line:
                parts = line.split(":", 1)
                key = parts[0].strip()
                value = parts[1].strip()
                if key and value:
                    key_value_pairs.append(
                        KeyValuePair(
                            key=key, value=value, confidence=0.9
                        )  # Confidence is simulated
                    )

    return key_value_pairs
