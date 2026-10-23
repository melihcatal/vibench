import os
from typing import List, Dict
from vision_client import AWSVisionClient
from vision_models import normalize_moderation_labels


def score_image_safety(image_path: str) -> Dict[str, List[dict]]:
    """Check an image for unsafe or policy-sensitive visual content using AWS Rekognition."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    client = AWSVisionClient()
    response = client.detect_moderation_labels(image_bytes)
    normalized_response = normalize_moderation_labels(response)

    unsafe_categories = {
        "Explicit Nudity": [],
        "Suggestive": [],
        "Violence": [],
        "Visually Disturbing": [],
        "Rude Gestures": [],
        "Drugs": [],
        "Tobacco": [],
        "Alcohol": [],
        "Gambling": [],
        "Hate Symbols": [],
    }

    for label in normalized_response.ModerationLabels:
        parent = label["ParentName"]
        if parent in unsafe_categories:
            unsafe_categories[parent].append(
                {"label": label["Name"], "confidence": label["Confidence"]}
            )

    return {"unsafe_content": unsafe_categories}
