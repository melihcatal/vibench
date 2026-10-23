import json
import os
from typing import Any, Dict

import requests

from vision_client import get_vision_api_key, get_vision_endpoint, image_to_data_url
from vision_models import ImageDescriptionRequest, ImageDescriptionResponse

AZURE_VISION_DESCRIPTION_PATH = "/computervision/imageanalysis:analyze"
AZURE_VISION_API_VERSION = "2024-02-01"


def describe_image(image_path: str, max_sentences: int = 2) -> ImageDescriptionResponse:
    req = ImageDescriptionRequest(image_path=image_path, max_sentences=max_sentences)
    endpoint = get_vision_endpoint().rstrip("/")
    url = f"{endpoint}{AZURE_VISION_DESCRIPTION_PATH}"
    headers = {
        "Ocp-Apim-Subscription-Key": get_vision_api_key(),
        "Content-Type": "application/json",
    }
    payload = {
        "url": image_to_data_url(req.image_path),
        "features": ["caption"],
        "language": "en",
    }
    response = requests.post(url, params={"api-version": AZURE_VISION_API_VERSION}, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    caption = data.get("caption", {}).get("text", "")
    confidence = data.get("caption", {}).get("confidence", 0.0)
    if max_sentences <= 1 and caption:
        caption = caption.split(".")[0].strip() + "."
    return ImageDescriptionResponse(description=caption, confidence=confidence, raw=data)


def main() -> None:
    image_path = os.environ.get("IMAGE_PATH", "")
    if not image_path:
        raise ValueError("IMAGE_PATH is required")
    result = describe_image(image_path)
    print(json.dumps(result.model_dump(), ensure_ascii=False))


if __name__ == "__main__":
    main()
