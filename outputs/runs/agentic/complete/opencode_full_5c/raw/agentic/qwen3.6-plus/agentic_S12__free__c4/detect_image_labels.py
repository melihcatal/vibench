from vision_client import (
    get_vision_client,
    build_vision_payload,
    parse_vision_response,
    VISION_MODEL,
)
from vision_models import ImageLabel, normalize_labels

VISION_MODEL_ID = "gpt-4o"

PROMPT_TEMPLATE = (
    "Analyze the provided image and return a list of detected labels or objects. "
    "Format each label on a new line as: label_name, confidence_score (0.0-1.0), category. "
    "Return at most 20 labels. Do not include any other text."
)


def detect_image_labels(
    image_url: str = None, image_base64: str = None
) -> list[ImageLabel]:
    client = get_vision_client()
    payload = build_vision_payload(
        image_url=image_url,
        image_base64=image_base64,
        prompt=PROMPT_TEMPLATE,
    )
    response = client.chat.completions.create(**payload)
    raw_text = parse_vision_response(response)
    labels = normalize_labels(raw_text)
    return labels


if __name__ == "__main__":
    import sys

    image_source = sys.argv[1] if len(sys.argv) > 1 else None
    if image_source and image_source.startswith("http"):
        result = detect_image_labels(image_url=image_source)
    elif image_source:
        import base64

        with open(image_source, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        result = detect_image_labels(image_base64=b64)
    else:
        raise ValueError("Provide image URL or file path")
    for label in result:
        print(f"{label.name}: {label.confidence:.2f} [{label.category}]")
