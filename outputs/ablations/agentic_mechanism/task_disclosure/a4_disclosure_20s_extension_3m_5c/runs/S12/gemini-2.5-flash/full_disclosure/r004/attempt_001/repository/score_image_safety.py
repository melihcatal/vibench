
from google.cloud import vision

def score_image_safety(image_content: bytes) -> dict:
    """
    Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision AI.

    Args:
        image_content: The content of the image as bytes.

    Returns:
        A dictionary containing the safety annotation results.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    # Convert the enum values to strings for easier interpretation
    likelihood_name = [
        'UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'
    ]

    safety_scores = {
        "adult": likelihood_name[safe_search_annotation.adult],
        "spoof": likelihood_name[safe_search_annotation.spoof],
        "medical": likelihood_name[safe_search_annotation.medical],
        "violence": likelihood_name[safe_search_annotation.violence],
        "racy": likelihood_name[safe_search_annotation.racy],
    }

    return safety_scores
