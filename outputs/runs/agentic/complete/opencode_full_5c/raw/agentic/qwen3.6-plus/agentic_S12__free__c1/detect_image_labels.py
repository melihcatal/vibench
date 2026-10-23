from __future__ import annotations

from typing import Optional

from vision_client import (
    VISION_MODEL_ID,
    build_vision_message,
    call_vision_api_with_json,
    get_openai_client,
    parse_labels_from_json,
)
from vision_models import ImageInput, LabelResponse, build_image_url_input

LABEL_DETECTION_PROMPT = """Analyze the provided image and detect all visible objects, labels, and entities.
Return a JSON object with a "labels" array. Each element must have:
- "name": string label of the detected object or entity
- "confidence": float between 0.0 and 1.0
- "bounding_box": optional object with "x", "y", "width", "height" (normalized 0-1)

Example: {"labels": [{"name": "person", "confidence": 0.95, "bounding_box": {"x": 0.1, "y": 0.2, "width": 0.3, "height": 0.5}}]}"""


def detect_image_labels(
    image_path: Optional[str] = None,
    image_url: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = VISION_MODEL_ID,
) -> LabelResponse:
    image_input = build_image_url_input(image_path=image_path, image_url=image_url)
    client = get_openai_client(api_key=api_key)
    messages = build_vision_message(image_input, LABEL_DETECTION_PROMPT, detail="high")
    raw_json = call_vision_api_with_json(client, messages, model=model, max_tokens=2048)
    image_id = image_path or image_url or ""
    return parse_labels_from_json(raw_json, image_id=image_id)


if __name__ == "__main__":
    import sys

    result = detect_image_labels(image_path=sys.argv[1] if len(sys.argv) > 1 else None)
    print(result)
