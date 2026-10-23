from __future__ import annotations

from vision_client import (
    get_openai_client,
    build_vision_messages,
    call_vision_api,
    DEFAULT_VISION_MODEL,
)
from vision_models import (
    ImageLabelRequest,
    ImageLabelResponse,
    normalize_label_response,
)


LABEL_SYSTEM_PROMPT = (
    "You are an image-labeling assistant powered by the OpenAI gpt-4o vision model. "
    "Analyze the provided image and return a JSON array of detected labels or objects. "
    "Each entry must have 'name' (string), 'confidence' (float 0.0-1.0), and 'category' (string). "
    "Return only valid JSON with no extra text."
)

LABEL_USER_PROMPT = (
    "Detect and label all visible objects, scenes, and concepts in this image. "
    "Return up to {max_labels} labels with confidence >= {confidence_threshold}."
)


def detect_image_labels(
    image_path: str,
    max_labels: int = 20,
    confidence_threshold: float = 0.0,
    model: str = DEFAULT_VISION_MODEL,
) -> ImageLabelResponse:
    request = ImageLabelRequest(
        image_path=image_path,
        max_labels=max_labels,
        confidence_threshold=confidence_threshold,
    )
    user_prompt = LABEL_USER_PROMPT.format(
        max_labels=request.max_labels,
        confidence_threshold=request.confidence_threshold,
    )
    messages = build_vision_messages(
        system_prompt=LABEL_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        image_path=request.image_path,
    )
    raw_text = call_vision_api(messages, model=model)
    return normalize_label_response(raw_text, request.image_path)


def detect_image_labels_batch(
    image_paths: list[str],
    max_labels: int = 20,
    confidence_threshold: float = 0.0,
    model: str = DEFAULT_VISION_MODEL,
) -> list[ImageLabelResponse]:
    client = get_openai_client()
    results: list[ImageLabelResponse] = []
    for path in image_paths:
        resp = detect_image_labels(
            image_path=path,
            max_labels=max_labels,
            confidence_threshold=confidence_threshold,
            model=model,
        )
        results.append(resp)
    return results


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "sample.jpg"
    result = detect_image_labels(path)
    for label in result.labels:
        print(f"{label.name}: {label.confidence:.2f} [{label.category}]")
