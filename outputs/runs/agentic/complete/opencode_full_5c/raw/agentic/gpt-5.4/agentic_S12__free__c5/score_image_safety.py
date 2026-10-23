from __future__ import annotations

from vision_client import encode_data_url, post_openai_json
from vision_models import ImageInput, ImageSafetyResult, normalize_openai_moderation


def score_image_safety(image_input: ImageInput) -> ImageSafetyResult:
    payload = {
        "model": "omni-moderation-latest",
        "input": [
            {
                "type": "image_url",
                "image_url": {
                    "url": encode_data_url(image_input),
                },
            }
        ],
    }
    response = post_openai_json("moderations", payload)
    return normalize_openai_moderation(response)
