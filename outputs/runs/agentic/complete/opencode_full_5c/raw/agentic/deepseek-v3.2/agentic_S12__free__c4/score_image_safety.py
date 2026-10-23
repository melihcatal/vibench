import os
import requests
from typing import Dict, Any


def score_image_safety(image_path: str) -> Dict[str, Any]:
    """
    Checks an image for unsafe or policy-sensitive visual content using Azure Computer Vision.

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary containing safety scores and categories
    """
    endpoint = os.environ.get("AZURE_VISION_ENDPOINT")
    subscription_key = os.environ.get("AZURE_VISION_KEY")

    if not endpoint or not subscription_key:
        raise ValueError(
            "AZURE_VISION_ENDPOINT and AZURE_VISION_KEY environment variables are required"
        )

    analyze_url = f"{endpoint}/vision/v3.2/analyze"

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/octet-stream",
    }

    params = {"visualFeatures": "Adult", "language": "en"}

    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data
    )

    if response.status_code != 200:
        raise Exception(
            f"Azure Computer Vision API error: {response.status_code} - {response.text}"
        )

    analysis = response.json()

    adult_info = analysis.get("adult", {})

    return {
        "is_adult_content": adult_info.get("isAdultContent", False),
        "is_racy_content": adult_info.get("isRacyContent", False),
        "is_gory_content": adult_info.get("isGoryContent", False),
        "adult_score": adult_info.get("adultScore", 0.0),
        "racy_score": adult_info.get("racyScore", 0.0),
        "gore_score": adult_info.get("goreScore", 0.0),
        "provider": "azure-computer-vision",
        "model_version": "3.2",
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python score_image_safety.py <image_path>")
        sys.exit(1)

    try:
        safety_scores = score_image_safety(sys.argv[1])
        print(
            f"Adult content: {safety_scores['is_adult_content']} (score: {safety_scores['adult_score']:.3f})"
        )
        print(
            f"Racy content: {safety_scores['is_racy_content']} (score: {safety_scores['racy_score']:.3f})"
        )
        print(
            f"Gory content: {safety_scores['is_gory_content']} (score: {safety_scores['gore_score']:.3f})"
        )
        print(f"Provider: {safety_scores['provider']}")
    except Exception as e:
        print(f"Error: {e}")
