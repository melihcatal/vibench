from google.cloud import vision

def extract_text(image_path: str) -> str:
    """Extracts plain text from a scanned document image."""
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts[0].description
    return ""
