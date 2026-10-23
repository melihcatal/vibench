import os
from typing import Optional
import requests
from vision_models import ImageDescriptionResponse


def describe_image(image_path: str, max_tokens: int = 64) -> ImageDescriptionResponse:
    """Generates a short visual description for an image using Azure AI Vision."""
    endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    key = os.getenv("AZURE_VISION_KEY")
    api_version = "2023-02-01-preview"
    url = f"{endpoint}/computervision/imageanalysis:analyze?api-version={api_version}&features=caption"

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/octet-stream"
    }

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    response = requests.post(url, headers=headers, data=image_data)
    response.raise_for_status()
    result = response.json()

    caption = result.get("captionResult", {}).get("text", "")
    confidence = result.get("captionResult", {}).get("confidence", 0.0)

    return ImageDescriptionResponse(
        description=caption,
        confidence=confidence
    )