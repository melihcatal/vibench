import os
from google.cloud import vision_v1p4beta1 as vision

def extract_text(image_content: bytes) -> str:
    """Extracts plain text from a scanned document image using Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts[0].description
    return ""

if __name__ == '__main__':
    # This is a placeholder for local testing
    # In a real scenario, you would load an image, e.g., from a file
    # For example:
    # with open("path/to/your/image.jpg", "rb") as image_file:
    #     content = image_file.read()
    #     extracted = extract_text(content)
    #     print("Extracted Text:", extracted)
    pass
