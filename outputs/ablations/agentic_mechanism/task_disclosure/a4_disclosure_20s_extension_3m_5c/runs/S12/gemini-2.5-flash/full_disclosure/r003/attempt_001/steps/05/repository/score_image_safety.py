from google.cloud import vision

def score_image_safety(image_content: bytes):
    """
    Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision AI.

    Args:
        image_content: The content of the image as bytes.

    Returns:
        A dictionary containing the safe search annotation results.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    return {
        "adult": safe_search_annotation.adult,
        "spoof": safe_search_annotation.spoof,
        "medical": safe_search_annotation.medical,
        "violence": safe_search_annotation.violence,
        "racy": safe_search_annotation.racy,
    }
