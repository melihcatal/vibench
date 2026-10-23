from typing import Dict, List

from openai import OpenAI

from vision_models import normalize_description

client = OpenAI()
MODEL_ID = "gpt-4o-mini"


def image_summary(labels: List[Dict[str, object]], description: str, text_blocks: List[Dict[str, object]]) -> str:
    prompt = {
        "labels": labels,
        "description": normalize_description(description),
        "text_blocks": text_blocks,
    }
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {"role": "system", "content": "Summarize image analysis results in one short paragraph."},
            {"role": "user", "content": str(prompt)},
        ],
    )
    return response.output_text
