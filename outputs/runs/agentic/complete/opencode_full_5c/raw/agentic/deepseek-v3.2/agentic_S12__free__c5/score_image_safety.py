import os
import requests
from typing import Dict, Any


def score_image_safety(image_path: str) -> Dict[str, Any]:
    """Check an image for unsafe or policy-sensitive visual content using Azure Content Safety."""
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required"
        )

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    import base64

    base64_image = base64.b64encode(image_data).decode("utf-8")

    headers = {"Content-Type": "application/json", "Ocp-Apim-Subscription-Key": api_key}

    payload = {
        "image": {"content": base64_image},
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
    }

    response = requests.post(
        f"{endpoint}/contentsafety/image:analyze?api-version=2023-10-01",
        headers=headers,
        json=payload,
    )

    if response.status_code != 200:
        raise Exception(
            f"Azure Content Safety API error: {response.status_code} - {response.text}"
        )

    result = response.json()

    safety_scores = {}
    for category_result in result.get("categoriesAnalysis", []):
        category = category_result["category"]
        safety_scores[category] = {
            "severity": category_result.get("severity", 0),
            "score": category_result.get("confidenceScore", 0),
        }

    return {
        "safety_scores": safety_scores,
        "is_safe": all(score["severity"] == 0 for score in safety_scores.values()),
    }
