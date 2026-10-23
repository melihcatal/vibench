import os
from typing import Optional

from openai import OpenAI

from vision_client import build_openai_client, image_input_from_path_or_bytes
from vision_models import SafetyResult, normalize_safety_result

MODEL_ID = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")


def score_image_safety(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None, client: Optional[OpenAI] = None) -> SafetyResult:
    client = client or build_openai_client()
    image_input = image_input_from_path_or_bytes(image_path=image_path, image_bytes=image_bytes)
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {
                "role": "system",
                "content": "Assess the image for safety-sensitive content and return a concise policy-style safety summary with risk levels.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Evaluate this image for unsafe or policy-sensitive content."},
                    {"type": "input_image", "image_url": image_input},
                ],
            },
        ],
        temperature=0,
    )
    return normalize_safety_result(response.output_text)
