from google.cloud import vision

def detect_text_from_image(image_content):
    """Detects text in an image.

    Args:
        image_content: The content of the image file as bytes.

    Returns:
        A string containing the detected text, or an empty string if no text is found.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        # The first annotation is the overall text detected in the image
        return texts[0].description
    else:
        return ""
