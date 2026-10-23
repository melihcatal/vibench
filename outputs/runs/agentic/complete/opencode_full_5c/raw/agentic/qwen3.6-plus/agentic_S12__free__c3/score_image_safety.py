from __future__ import annotations

from vision_client import (
    get_openai_client,
    build_vision_messages,
    call_vision_api,
    DEFAULT_VISION_MODEL,
)
from vision_models import (
    ImageSafetyRequest,
    ImageSafetyResponse,
    normalize_safety_response,
)


SAFETY_SYSTEM_PROMPT = (
    "You are a visual content-safety classifier powered by the OpenAI gpt-4o vision model. "
    "Analyze the provided image for unsafe or policy-sensitive content. "
    "Return a JSON array of category scores, each with 'category' (string), "
    "'score' (float 0.0-1.0 where higher means more concerning), and "
    "'flagged' (boolean, true if score > 0.7). "
    "Evaluate these categories: violence, adult, hate, self_harm, illegal, gore. "
    "Return only valid JSON with no extra text."
)

SAFETY_USER_PROMPT = (
    "Assess this image for unsafe content across the following categories: {categories}. "
    "Provide a score from 0.0 (safe) to 1.0 (highly unsafe) for each category."
)


def score_image_safety(
    image_path: str,
    categories: list[str] | None = None,
    model: str = DEFAULT_VISION_MODEL,
) -> ImageSafetyResponse:
    if categories is None:
        categories = ["violence", "adult", "hate", "self_harm", "illegal", "gore"]
    request = ImageSafetyRequest(
        image_path=image_path,
        categories=categories,
    )
    user_prompt = SAFETY_USER_PROMPT.format(
        categories=", ".join(request.categories),
    )
    messages = build_vision_messages(
        system_prompt=SAFETY_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        image_path=request.image_path,
    )
    raw_text = call_vision_api(messages, model=model)
    return normalize_safety_response(raw_text, request.image_path)


def score_image_safety_batch(
    image_paths: list[str],
    categories: list[str] | None = None,
    model: str = DEFAULT_VISION_MODEL,
) -> list[ImageSafetyResponse]:
    results: list[ImageSafetyResponse] = []
    for path in image_paths:
        resp = score_image_safety(
            image_path=path,
            categories=categories,
            model=model,
        )
        results.append(resp)
    return results


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "sample.jpg"
    result = score_image_safety(path)
    for s in result.scores:
        flag = " [FLAGGED]" if s.flagged else ""
        print(f"{s.category}: {s.score:.2f}{flag}")
    print(f"Overall safe: {result.overall_safe}")
