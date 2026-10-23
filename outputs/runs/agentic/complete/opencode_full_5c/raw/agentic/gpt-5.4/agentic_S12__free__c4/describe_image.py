from __future__ import annotations

from vision_client import build_data_url, get_openai_client, load_image_input
from vision_models import ImageDescriptionResult


OPENAI_VISION_MODEL = "gpt-4.1-mini"


def describe_image(
    image_path: str, mime_type: str = "image/jpeg"
) -> ImageDescriptionResult:
    client = get_openai_client()
    image = load_image_input(image_path, mime_type=mime_type)
    response = client.responses.create(
        model=OPENAI_VISION_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Describe this image in one short sentence.",
                    },
                    {"type": "input_image", "image_url": build_data_url(image)},
                ],
            }
        ],
    )
    return ImageDescriptionResult(
        provider="openai",
        description=response.output_text.strip(),
        model=OPENAI_VISION_MODEL,
    )
