from google.cloud import vision

def extract_text_from_image(image_content: bytes) -> str:
    """
    Extracts plain text from a scanned document image using Google Cloud Vision AI.

    Args:
        image_content: The content of the image file as bytes.

    Returns:
        The extracted plain text from the image.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        # The first text annotation is the full text of the document
        full_text = texts[0].description
        return full_text
    else:
        return ""

