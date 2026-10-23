import json
from typing import Any, Dict, List

from openai import OpenAI

from vision_client import load_vision_config


def summarize_visual_analysis(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    config = load_vision_config()
    client = OpenAI(api_key=config.openai_api_key, base_url=config.openai_base_url)
    response = client.responses.create(
        model=config.vision_model,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Summarize these visual analysis results into one short paragraph and a concise bullets array."},
                    {"type": "input_text", "text": json.dumps(results, ensure_ascii=False)},
                ],
            }
        ],
        temperature=0.2,
    )
    return {"provider": "openai", "model": config.vision_model, "summary": response.output_text.strip()}
