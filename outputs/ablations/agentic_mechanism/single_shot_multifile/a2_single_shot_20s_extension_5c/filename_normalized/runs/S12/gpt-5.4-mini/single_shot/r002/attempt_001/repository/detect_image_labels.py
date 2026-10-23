import base64
import os
from typing import Any, Dict, List

from openai import OpenAI

from vision_client import load_vision_config, read_image_bytes, to_data_url
from vision_models import coerce_label_list, normalize_label_result


def detect_image_labels(image_path: str, max_labels: int = 8) -> Dict[str, Any]:
    config = load_vision_config()
    client = OpenAI(api_key=config.openai_api_key, base_url=config.openai_base_url)
    image_bytes = read_image_bytes(image_path)
    data_url = to_data_url(image_bytes, mime_type=config.mime_type)
    prompt = (
        "Return only a concise JSON object with a labels array of short object or scene labels "
        "for the image. Prefer concrete visible entities."
    )
    response = client.responses.create(
        model=config.vision_model,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": data_url},
                ],
            }
        ],
        temperature=0,
    )
    text = response.output_text
    labels = coerce_label_list(text, max_labels=max_labels)
    return normalize_label_result(labels, provider="openai", model=config.vision_model)
