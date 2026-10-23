import os
from google.cloud import vision

def extract_text(image_content: bytes) -> str:
    """Extracts plain text from a scanned document image using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.document_text_detection(image=image)
    return response.full_text_annotation.text

if __name__ == '__main__':
    # Example usage (replace with actual image content)
    # For a real scenario, load image_content from a file or byte stream.
    # For demonstration, using a placeholder.
    _dummy_image_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82"
    _text = extract_text(_dummy_image_content)
    print(f"Extracted Text: {_text}")
