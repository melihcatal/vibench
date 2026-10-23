from __future__ import annotations

from vision_client import (
    get_openai_client,
    build_vision_messages,
    call_vision_api,
    DEFAULT_VISION_MODEL,
)
from vision_models import (
    ImageDescriptionRequest,
    ImageDescriptionResponse,
    normalize_description_response,
)


DESCRIBE_SYSTEM_PROMPT = (
    "You are an image-description assistant powered by the OpenAI gpt-4o vision model. "
    "Generate a concise, accurate visual description of the provided image. "
    "Focus on main subjects, setting, colors, and notable visual details. "
    "Keep the description within the specified length."
)

DESCRIBE_USER_PROMPT = (
    "Describe this image in {detail_level} detail, using at most {max_length} words. "
    "Focus on what is visually present: objects, people, setting, colors, and composition."
)


def describe_image(
    image_path: str,
    max_length: int = 150,
    detail_level: str = "brief",
    model: str = DEFAULT_VISION_MODEL,
) -> ImageDescriptionResponse:
    request = ImageDescriptionRequest(
        image_path=image_path,
        max_length=max_length,
        detail_level=detail_level,
    )
    user_prompt = DESCRIBE_USER_PROMPT.format(
        max_length=request.max_length,
        detail_level=request.detail_level,
    )
    messages = build_vision_messages(
        system_prompt=DESCRIBE_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        image_path=request.image_path,
    )
    raw_text = call_vision_api(messages, model=model)
    return normalize_description_response(raw_text, request.image_path)


def describe_image_batch(
    image_paths: list[str],
    max_length: int = 150,
    detail_level: str = "brief",
    model: str = DEFAULT_VISION_MODEL,
) -> list[ImageDescriptionResponse]:
    results: list[ImageDescriptionResponse] = []
    for path in image_paths:
        resp = describe_image(
            image_path=path,
            max_length=max_length,
            detail_level=detail_level,
            model=model,
        )
        results.append(resp)
    return results


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "sample.jpg"
    result = describe_image(path)
    print(result.description)
