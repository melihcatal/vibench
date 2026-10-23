from __future__ import annotations

from vision_client import (
    OPENAI_MODEL,
    get_openai_client,
    image_to_data_url,
    load_image_input,
)
from vision_models import ImageDescriptionResult


def describe_image(
    image_path: str, prompt: str = "Describe this image in one short sentence."
) -> dict:
    image_input = load_image_input(image_path=image_path)
    client = get_openai_client()
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": image_to_data_url(image_input),
                    },
                ],
            }
        ],
    )
    return ImageDescriptionResult(
        provider="openai", description=response.output_text.strip(), model=OPENAI_MODEL
    ).to_dict()
