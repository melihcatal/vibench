from vision_client import (
    get_vision_client,
    build_vision_payload,
    parse_vision_response,
    VISION_MODEL,
)
from vision_models import DetectedText, normalize_detected_text

VISION_MODEL_ID = "gpt-4o"

PROMPT_TEMPLATE = (
    "Extract all visible text from the provided image. "
    "Return each distinct text segment on a separate line. "
    "Preserve the original language and punctuation. "
    "If no text is visible, return an empty response."
)


def detect_image_text(
    image_url: str = None, image_base64: str = None
) -> list[DetectedText]:
    client = get_vision_client()
    payload = build_vision_payload(
        image_url=image_url,
        image_base64=image_base64,
        prompt=PROMPT_TEMPLATE,
    )
    response = client.chat.completions.create(**payload)
    raw_text = parse_vision_response(response)
    texts = normalize_detected_text(raw_text)
    return texts


if __name__ == "__main__":
    import sys

    image_source = sys.argv[1] if len(sys.argv) > 1 else None
    if image_source and image_source.startswith("http"):
        result = detect_image_text(image_url=image_source)
    elif image_source:
        import base64

        with open(image_source, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        result = detect_image_text(image_base64=b64)
    else:
        raise ValueError("Provide image URL or file path")
    for text in result:
        print(text.text)
