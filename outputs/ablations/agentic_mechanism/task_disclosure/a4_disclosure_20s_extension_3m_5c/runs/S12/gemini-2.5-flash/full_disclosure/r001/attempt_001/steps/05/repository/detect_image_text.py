from google.cloud import vision

def detect_image_text(image_content: bytes):
    """Detects text in an image using Google Cloud Vision AI.

    Args:
        image_content: The image content as bytes.

    Returns:
        A list of strings, where each string is a detected text annotation.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = [text.description for text in response.text_annotations]
    return texts
