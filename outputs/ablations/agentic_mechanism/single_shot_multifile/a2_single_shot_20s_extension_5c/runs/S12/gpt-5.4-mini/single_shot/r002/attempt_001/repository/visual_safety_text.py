from typing import Any, Dict

from openai import OpenAI

from vision_client import load_vision_config


def check_visual_labels_for_unsafe_text(labels: str) -> Dict[str, Any]:
    config = load_vision_config()
    client = OpenAI(api_key=config.openai_api_key, base_url=config.openai_base_url)
    response = client.responses.create(
        model=config.vision_model,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Review these generated visual labels for unsafe or policy-sensitive text. Return a short verdict and reasons if needed."},
                    {"type": "input_text", "text": labels},
                ],
            }
        ],
        temperature=0,
    )
    return {"provider": "openai", "model": config.vision_model, "verdict": response.output_text.strip()}
