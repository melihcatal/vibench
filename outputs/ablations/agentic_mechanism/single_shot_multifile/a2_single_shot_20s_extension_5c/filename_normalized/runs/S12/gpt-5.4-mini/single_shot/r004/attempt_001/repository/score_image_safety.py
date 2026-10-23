import os
from typing import Any, Dict, Optional

from vision_client import build_openai_client, image_to_data_url
from vision_models import SafetyResult, normalize_safety_label

_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")


def score_image_safety(image_path: Optional[str] = None, image_bytes: Optional[bytes] = None, image_url: Optional[str] = None) -> Dict[str, Any]:
    client = build_openai_client()
    data_url = image_to_data_url(image_path=image_path, image_bytes=image_bytes, image_url=image_url)
    prompt = "Assess whether this image contains unsafe, policy-sensitive, explicit, violent, hateful, or otherwise concerning visual content. Return a short risk label and brief rationale."
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
    label = normalize_safety_label(text)
    return SafetyResult(label=label, rationale=text.strip(), raw_text=text).to_dict()
