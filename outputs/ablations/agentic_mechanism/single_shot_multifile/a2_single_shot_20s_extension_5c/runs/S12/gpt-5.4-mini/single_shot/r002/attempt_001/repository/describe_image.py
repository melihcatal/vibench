from typing import Any, Dict

from openai import OpenAI

from vision_client import load_vision_config, read_image_bytes, to_data_url
from vision_models import normalize_description_result


def describe_image(image_path: str, max_chars: int = 240) -> Dict[str, Any]:
    config = load_vision_config()
    client = OpenAI(api_key=config.openai_api_key, base_url=config.openai_base_url)
    image_bytes = read_image_bytes(image_path)
    data_url = to_data_url(image_bytes, mime_type=config.mime_type)
    response = client.responses.create(
        model=config.vision_model,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Write a short visual description of this image."},
                    {"type": "input_image", "image_url": data_url},
                ],
            }
        ],
        temperature=0.2,
    )
    return normalize_description_result(response.output_text, provider="openai", model=config.vision_model, max_chars=max_chars)
