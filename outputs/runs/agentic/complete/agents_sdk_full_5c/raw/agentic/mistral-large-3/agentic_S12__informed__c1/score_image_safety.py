import os
import requests
from vision_models import ImageSafetyResponse


def score_image_safety(image_path: str) -> ImageSafetyResponse:
    """Check an image for unsafe or policy-sensitive content using Azure AI Content Safety."""
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    url = f"{endpoint}/contentsafety/image:analyze?api-version=2023-10-01"

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/octet-stream"
    }

    response = requests.post(url, headers=headers, data=image_data)
    response.raise_for_status()
    result = response.json()

    categories = [
        "Hate", "SelfHarm", "Sexual", "Violence"
    ]
    scores = {category: 0.0 for category in categories}

    for item in result.get("categoriesAnalysis", []):
        category = item.get("category")
        severity = item.get("severity", 0)
        if category in scores:
            scores[category] = severity / 6.0  # Normalize to 0-1

    return ImageSafetyResponse(
        is_safe=all(score < 0.5 for score in scores.values()),
        safety_scores=scores
    )