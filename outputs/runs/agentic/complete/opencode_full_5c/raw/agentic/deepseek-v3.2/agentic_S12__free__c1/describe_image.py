import os
import requests
from vision_client import get_azure_vision_key, get_azure_vision_endpoint


def describe_image(image_path: str) -> str:
    """Generates a short visual description for an image using Azure Computer Vision."""
    subscription_key = get_azure_vision_key()
    endpoint = get_azure_vision_endpoint()

    analyze_url = f"{endpoint}/vision/v3.2/describe"

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Content-Type": "application/octet-stream",
    }

    params = {"maxCandidates": 1, "language": "en"}

    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data
    )
    response.raise_for_status()

    analysis = response.json()

    if "description" in analysis and "captions" in analysis["description"]:
        captions = analysis["description"]["captions"]
        if captions:
            return captions[0]["text"]

    return "No description generated"


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python describe_image.py <image_path>")
        sys.exit(1)

    description = describe_image(sys.argv[1])
    print(f"Image description: {description}")
