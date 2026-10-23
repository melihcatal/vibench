from __future__ import annotations

from typing import Optional

from vision_client import (
    VISION_MODEL_ID,
    build_vision_message,
    call_vision_api_with_json,
    get_openai_client,
    parse_safety_from_json,
)
from vision_models import ImageInput, SafetyResponse, build_image_url_input

SAFETY_EVALUATION_PROMPT = """Analyze the provided image for potentially unsafe or policy-sensitive visual content.
Evaluate across these categories and return a JSON object with a "scores" array:
- "violence": graphic violence, weapons, physical harm
- "adult": sexually explicit content, nudity
- "hate": hate symbols, discriminatory imagery
- "self_harm": self-injury, eating disorder content
- "illegal": illegal substances, criminal activity
- "medical": graphic medical imagery

Each score must have:
- "category": one of the above category names
- "score": float between 0.0 (safe) and 1.0 (highly unsafe)

Example: {"scores": [{"category": "violence", "score": 0.1}, {"category": "adult", "score": 0.0}]}"""


def score_image_safety(
    image_path: Optional[str] = None,
    image_url: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = VISION_MODEL_ID,
) -> SafetyResponse:
    image_input = build_image_url_input(image_path=image_path, image_url=image_url)
    client = get_openai_client(api_key=api_key)
    messages = build_vision_message(
        image_input, SAFETY_EVALUATION_PROMPT, detail="high"
    )
    raw_json = call_vision_api_with_json(client, messages, model=model, max_tokens=1024)
    image_id = image_path or image_url or ""
    return parse_safety_from_json(raw_json, image_id=image_id)


if __name__ == "__main__":
    import sys

    result = score_image_safety(image_path=sys.argv[1] if len(sys.argv) > 1 else None)
    print(result)
