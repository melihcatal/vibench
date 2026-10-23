import base64
import json
import os
from typing import Any, Dict, Optional

import requests

from vision_client import get_vision_api_key, get_vision_endpoint, image_to_data_url
from vision_models import ImageLabelDetectionRequest, ImageLabelDetectionResponse, normalize_label_items

AZURE_VISION_RECOGNITION_PATH = "/computervision/imageanalysis:analyze"
AZURE_VISION_API_VERSION = "2024-02-01"


def detect_image_labels(image_path: str, max_labels: int = 10, language: str = "en") -> ImageLabelDetectionResponse:
    req = ImageLabelDetectionRequest(image_path=image_path, max_labels=max_labels, language=language)
    endpoint = get_vision_endpoint().rstrip("/")
    api_key = get_vision_api_key()
    url = f"{endpoint}{AZURE_VISION_RECOGNITION_PATH}"
    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "url": image_to_data_url(req.image_path),
        "features": ["tags"],
        "language": req.language,
    }
    response = requests.post(url, params={"api-version": AZURE_VISION_API_VERSION}, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    tags = data.get("tags", [])
    labels = normalize_label_items(tags, max_items=req.max_labels)
    return ImageLabelDetectionResponse(labels=labels, raw=data)


def main() -> None:
    image_path = os.environ.get("IMAGE_PATH", "")
    if not image_path:
        raise ValueError("IMAGE_PATH is required")
    result = detect_image_labels(image_path)
    print(json.dumps(result.model_dump(), ensure_ascii=False))


if __name__ == "__main__":
    main()
