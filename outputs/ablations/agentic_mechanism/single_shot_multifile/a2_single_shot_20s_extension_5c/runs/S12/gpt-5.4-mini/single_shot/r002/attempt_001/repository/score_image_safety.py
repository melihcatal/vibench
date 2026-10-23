from typing import Any, Dict

from openai import OpenAI

from vision_client import load_vision_config, read_image_bytes, to_data_url
from vision_models import normalize_safety_result


def score_image_safety(image_path: str) -> Dict[str, Any]:
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
                    {"type": "input_text", "text": "Assess whether the image contains unsafe, explicit, violent, self-harm, or policy-sensitive visual content. Return JSON with safe boolean and reasons array."},
                    {"type": "input_image", "image_url": data_url},
                ],
            }
        ],
        temperature=0,
    )
    return normalize_safety_result(response.output_text, provider="openai", model=config.vision_model)
