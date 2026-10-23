import os
import json
from vision_client import VisionClient


def detect_image_text(image_path: str) -> dict:
    """Detect readable text that appears inside an image.

    Provider: Alibaba Cloud Vision OCR (Optical Character Recognition).
    Identifiable via SDK import `alibabacloud_vision` and env vars for credentials.

    Args:
        image_path: Local file path to the image.

    Returns:
        Dict with keys:
            - 'text_blocks': list of detected strings.
            - 'raw_response': raw API output (optional, retained for debugging).
    """
    client = VisionClient()
    raw = client.extract_text(image_path)
    # The service returns a list of text blocks with confidence
    text_blocks = [block["content"] for block in raw.get("blocks", [])]
    return {"text_blocks": text_blocks, "raw_response": raw}


if __name__ == "__main__":
    img = "example.jpg"
    result = detect_image_text(img)
    print(json.dumps(result, ensure_ascii=False, indent=2))
