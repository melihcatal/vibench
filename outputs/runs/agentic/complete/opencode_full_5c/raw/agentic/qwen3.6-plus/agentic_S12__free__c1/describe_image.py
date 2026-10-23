from __future__ import annotations

from typing import Optional

from vision_client import (
    VISION_MODEL_ID,
    build_vision_message,
    call_vision_api,
    get_openai_client,
    parse_description_from_text,
)
from vision_models import DescriptionResponse, ImageInput, build_image_url_input

IMAGE_DESCRIPTION_PROMPT = """Provide a concise, accurate visual description of the image in 2-4 sentences.
Describe the main subjects, setting, colors, composition, and any notable details.
Be objective and avoid speculation about context not visible in the image."""


def describe_image(
    image_path: Optional[str] = None,
    image_url: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = VISION_MODEL_ID,
) -> DescriptionResponse:
    image_input = build_image_url_input(image_path=image_path, image_url=image_url)
    client = get_openai_client(api_key=api_key)
    messages = build_vision_message(
        image_input, IMAGE_DESCRIPTION_PROMPT, detail="high"
    )
    text = call_vision_api(client, messages, model=model, max_tokens=512)
    image_id = image_path or image_url or ""
    return parse_description_from_text(text, image_id=image_id)


if __name__ == "__main__":
    import sys

    result = describe_image(image_path=sys.argv[1] if len(sys.argv) > 1 else None)
    print(result)
