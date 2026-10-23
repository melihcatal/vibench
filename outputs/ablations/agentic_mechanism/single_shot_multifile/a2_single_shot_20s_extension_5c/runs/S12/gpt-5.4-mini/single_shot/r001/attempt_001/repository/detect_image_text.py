import json
import os
from typing import Any, Dict, List

import requests

from vision_client import get_vision_api_key, get_vision_endpoint, image_to_data_url
from vision_models import ImageTextDetectionRequest, ImageTextDetectionResponse, normalize_text_lines

AZURE_VISION_OCR_PATH = "/computervision/imageanalysis:analyze"
AZURE_VISION_API_VERSION = "2024-02-01"


def detect_image_text(image_path: str, language: str = "en") -> ImageTextDetectionResponse:
    req = ImageTextDetectionRequest(image_path=image_path, language=language)
    endpoint = get_vision_endpoint().rstrip("/")
    url = f"{endpoint}{AZURE_VISION_OCR_PATH}"
    headers = {
        "Ocp-Apim-Subscription-Key": get_vision_api_key(),
        "Content-Type": "application/json",
    }
    payload = {
        "url": image_to_data_url(req.image_path),
        "features": ["read"],
        "language": req.language,
    }
    response = requests.post(url, params={"api-version": AZURE_VISION_API_VERSION}, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    lines: List[str] = normalize_text_lines(data.get("readResult", {}).get("blocks", []))
    return ImageTextDetectionResponse(text_lines=lines, raw=data)


def main() -> None:
    image_path = os.environ.get("IMAGE_PATH", "")
    if not image_path:
        raise ValueError("IMAGE_PATH is required")
    result = detect_image_text(image_path)
    print(json.dumps(result.model_dump(), ensure_ascii=False))


if __name__ == "__main__":
    main()
