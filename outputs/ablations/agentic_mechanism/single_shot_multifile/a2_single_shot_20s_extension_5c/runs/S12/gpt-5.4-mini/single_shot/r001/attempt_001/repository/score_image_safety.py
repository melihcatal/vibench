import json
import os
from typing import Any, Dict

import requests

from vision_client import get_vision_api_key, get_vision_endpoint, image_to_data_url
from vision_models import ImageSafetyRequest, ImageSafetyResponse

AZURE_VISION_SAFETY_PATH = "/computervision/imageanalysis:analyze"
AZURE_VISION_API_VERSION = "2024-02-01"


def score_image_safety(image_path: str) -> ImageSafetyResponse:
    req = ImageSafetyRequest(image_path=image_path)
    endpoint = get_vision_endpoint().rstrip("/")
    url = f"{endpoint}{AZURE_VISION_SAFETY_PATH}"
    headers = {
        "Ocp-Apim-Subscription-Key": get_vision_api_key(),
        "Content-Type": "application/json",
    }
    payload = {
        "url": image_to_data_url(req.image_path),
        "features": ["smartCrops", "tags"],
        "genderNeutralCaption": False,
    }
    response = requests.post(url, params={"api-version": AZURE_VISION_API_VERSION}, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    adult = data.get("adult", {})
    unsafe_score = float(adult.get("veryAdultScore", 0.0) or 0.0)
    safe = unsafe_score < 0.5 and not adult.get("isAdultContent", False) and not adult.get("isRacyContent", False)
    reasons = []
    if adult.get("isAdultContent", False):
        reasons.append("adult_content")
    if adult.get("isRacyContent", False):
        reasons.append("racy_content")
    return ImageSafetyResponse(safe=safe, unsafe_score=unsafe_score, reasons=reasons, raw=data)


def main() -> None:
    image_path = os.environ.get("IMAGE_PATH", "")
    if not image_path:
        raise ValueError("IMAGE_PATH is required")
    result = score_image_safety(image_path)
    print(json.dumps(result.model_dump(), ensure_ascii=False))


if __name__ == "__main__":
    main()
