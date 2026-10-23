from typing import Any, Dict

from openai import OpenAI

from vision_client import load_vision_config


def translate_alt_text(text: str, target_language: str) -> Dict[str, Any]:
    config = load_vision_config()
    client = OpenAI(api_key=config.openai_api_key, base_url=config.openai_base_url)
    response = client.responses.create(
        model=config.vision_model,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": f"Translate this image description into {target_language}. Preserve concise alt-text style."},
                    {"type": "input_text", "text": text},
                ],
            }
        ],
        temperature=0.2,
    )
    return {"provider": "openai", "model": config.vision_model, "text": response.output_text.strip()}
