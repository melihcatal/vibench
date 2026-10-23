from google.cloud import vision

def extract_text_from_image(image_content: bytes) -> str:
    """Extracts plain text from a scanned document image using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    return ""
