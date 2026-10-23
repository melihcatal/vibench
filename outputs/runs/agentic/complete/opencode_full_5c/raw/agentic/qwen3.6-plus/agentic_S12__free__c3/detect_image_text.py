from __future__ import annotations

from vision_client import (
    get_openai_client,
    build_vision_messages,
    call_vision_api,
    DEFAULT_VISION_MODEL,
)
from vision_models import (
    ImageTextRequest,
    ImageTextResponse,
    normalize_text_response,
)


TEXT_SYSTEM_PROMPT = (
    "You are an OCR and text-detection assistant powered by the OpenAI gpt-4o vision model. "
    "Extract all visible text from the provided image. "
    "Return a JSON array of text regions, each with 'text' (string), "
    "'bounding_box' (dict with x, y, width, height as floats 0.0-1.0 relative to image), "
    "'confidence' (float 0.0-1.0), and 'language' (string). "
    "Return only valid JSON with no extra text."
)

TEXT_USER_PROMPT = (
    "Extract all text visible in this image. "
    "Include bounding-box estimates and confidence scores for each text region. "
    "If a language hint is provided ({language_hint}), use it to guide detection."
)


def detect_image_text(
    image_path: str,
    language_hint: str | None = None,
    model: str = DEFAULT_VISION_MODEL,
) -> ImageTextResponse:
    request = ImageTextRequest(
        image_path=image_path,
        language_hint=language_hint,
    )
    user_prompt = TEXT_USER_PROMPT.format(
        language_hint=request.language_hint or "none",
    )
    messages = build_vision_messages(
        system_prompt=TEXT_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        image_path=request.image_path,
    )
    raw_text = call_vision_api(messages, model=model)
    return normalize_text_response(raw_text, request.image_path)


def detect_image_text_batch(
    image_paths: list[str],
    language_hint: str | None = None,
    model: str = DEFAULT_VISION_MODEL,
) -> list[ImageTextResponse]:
    results: list[ImageTextResponse] = []
    for path in image_paths:
        resp = detect_image_text(
            image_path=path,
            language_hint=language_hint,
            model=model,
        )
        results.append(resp)
    return results


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "sample.jpg"
    result = detect_image_text(path)
    print(result.full_text)
