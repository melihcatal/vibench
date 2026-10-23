import os
import base64
from typing import Dict, Any
import requests
from vision_client import get_azure_vision_key


def score_image_safety(image_path: str) -> Dict[str, Any]:
    """
    Check an image for unsafe or policy-sensitive visual content using Azure Computer Vision.

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary containing safety scores and analysis results
    """
    subscription_key, endpoint = get_azure_vision_key()

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": subscription_key,
    }

    params = {"visualFeatures": "Adult", "language": "en"}

    response = requests.post(
        f"{endpoint}/vision/v3.2/analyze",
        headers=headers,
        params=params,
        data=image_data,
    )
    response.raise_for_status()

    result = response.json()

    adult_info = result.get("adult", {})

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
