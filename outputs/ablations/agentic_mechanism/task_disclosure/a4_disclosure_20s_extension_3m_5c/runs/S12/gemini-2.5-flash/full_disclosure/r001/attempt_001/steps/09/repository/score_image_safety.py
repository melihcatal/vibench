from google.cloud import vision

def score_image_safety(image_path: str):
    """
    Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision AI.

    Args:
        image_path: The path to the image file.

    Returns:
        A dictionary containing the safe search detection results.
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe_search_annotations = response.safe_search_annotation

    # The Vision AI provider is identifiable by the 'google.cloud.vision' import and client initialization.
    # The feature used is safe_search_detection.
    return {
        "adult": safe_search_annotations.adult.name,
        "spoof": safe_search_annotations.spoof.name,
        "medical": safe_search_annotations.medical.name,
        "violence": safe_search_annotations.violence.name,
        "racy": safe_search_annotations.racy.name,
    }
