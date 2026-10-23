from google.cloud import vision
from document_client import get_document_client
from document_models import KeyValuePair


def extract_key_value_pairs(image_path: str) -> list[KeyValuePair]:
    """
    Extracts key-value pairs from a document image using Google Cloud Vision API.
    Note: This requires custom logic to find relationships between text entities.
    """
    client = get_document_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Provider-specific API call providing the text and layout data.
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(response.error.message)

    # Placeholder for key-value pair extraction logic.
    # A real implementation would iterate through the words and lines in
    # response.full_text_annotation, identifying patterns typical for forms.
    # For example, it might look for text ending in a colon (':') and then find
    # the nearest text block to its right on the same line.

    extracted_pairs = []

    return extracted_pairs
