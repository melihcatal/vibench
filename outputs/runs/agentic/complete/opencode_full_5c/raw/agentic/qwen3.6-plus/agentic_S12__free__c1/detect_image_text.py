from __future__ import annotations

from typing import Optional

from vision_client import (
    VISION_MODEL_ID,
    build_vision_message,
    call_vision_api_with_json,
    get_openai_client,
    parse_text_detection_from_json,
)
from vision_models import ImageInput, TextDetectionResponse, build_image_url_input

TEXT_DETECTION_PROMPT = """Detect and extract all visible text from the provided image.
Return a JSON object with:
- "full_text": a single string concatenating all detected text in reading order
- "regions": an array of text regions, each with:
  - "text": the detected text string
  - "confidence": float between 0.0 and 1.0
  - "language": ISO 639-1 language code (e.g., "en", "es", "zh")
  - "bounding_box": optional object with "x", "y", "width", "height" (normalized 0-1)

Example: {"full_text": "Hello World", "regions": [{"text": "Hello", "confidence": 0.98, "language": "en"}]}"""


def detect_image_text(
    image_path: Optional[str] = None,
    image_url: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = VISION_MODEL_ID,
) -> TextDetectionResponse:
    image_input = build_image_url_input(image_path=image_path, image_url=image_url)
    client = get_openai_client(api_key=api_key)
    messages = build_vision_message(image_input, TEXT_DETECTION_PROMPT, detail="high")
    raw_json = call_vision_api_with_json(client, messages, model=model, max_tokens=2048)
    image_id = image_path or image_url or ""
    return parse_text_detection_from_json(raw_json, image_id=image_id)


if __name__ == "__main__":
    import sys

    result = detect_image_text(image_path=sys.argv[1] if len(sys.argv) > 1 else None)
    print(result)
