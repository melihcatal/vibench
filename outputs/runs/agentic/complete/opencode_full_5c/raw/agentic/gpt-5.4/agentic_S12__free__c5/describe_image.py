from __future__ import annotations

from vision_client import encode_data_url, post_openai_json
from vision_models import (
    ImageDescriptionResult,
    ImageInput,
    normalize_openai_description,
)


def describe_image(image_input: ImageInput) -> ImageDescriptionResult:
    payload = {
        "model": "gpt-4.1-mini",
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Describe this image in one short sentence for accessibility alt text.",
                    },
                    {"type": "input_image", "image_url": encode_data_url(image_input)},
                ],
            }
        ],
    }
    response = post_openai_json("responses", payload)
    return normalize_openai_description(response)
