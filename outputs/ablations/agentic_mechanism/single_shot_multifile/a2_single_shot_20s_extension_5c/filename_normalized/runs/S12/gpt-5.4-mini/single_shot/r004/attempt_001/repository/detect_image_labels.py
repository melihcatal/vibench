import base64
import os
from typing import Any, Dict, Optional

from openai import OpenAI

from vision_client import build_openai_client, image_to_data_url
from vision_models import LabelDetectionResult, normalize_label_list

_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")


def detect_image_labels(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None, image_url: Optional[str] = None) -> Dict[str, Any]:
    client = build_openai_client()
    data_url = image_to_data_url(image_path=image_path, image_bytes=image_bytes, image_url=image_url)
    prompt = "Detect the main objects, entities, and scene labels visible in this image. Return concise labels only."
    response = client.responses.create(
        model=_MODEL,
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
    text = getattr(response, "output_text", "") or ""
    labels = normalize_label_list(text)
    result = LabelDetectionResult(labels=labels, raw_text=text)
    return result.to_dict()
