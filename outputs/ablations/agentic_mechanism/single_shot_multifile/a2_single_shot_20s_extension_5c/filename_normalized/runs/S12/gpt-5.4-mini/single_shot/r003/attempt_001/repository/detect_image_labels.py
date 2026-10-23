import base64
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

from vision_client import build_openai_client, image_input_from_path_or_bytes
from vision_models import ImageLabel, LabelResult, normalize_label_result

MODEL_ID = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")


def detect_image_labels(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None, client: Optional[OpenAI] = None) -> LabelResult:
    client = client or build_openai_client()
    image_input = image_input_from_path_or_bytes(image_path=image_path, image_bytes=image_bytes)
    response = client.responses.create(
        model=MODEL_ID,
        input=[
            {
                "role": "system",
                "content": "Identify the main objects, scenes, and visible entities in the image. Return concise labels with confidence estimates.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "List the most important labels for this image as JSON."},
                    {"type": "input_image", "image_url": image_input},
                ],
            },
        ],
        temperature=0,
    )
    text = response.output_text
    return normalize_label_result(text)
