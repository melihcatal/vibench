from __future__ import annotations

from vision_client import create_openai_client, to_data_url
from vision_models import ImageDescriptionResult, ImageInput


def describe_image(
    image: ImageInput,
    prompt: str = "Write a short factual description of this image in one sentence.",
) -> dict:
    client = create_openai_client()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": to_data_url(image)},
                ],
            }
        ],
    )
    description = response.output_text.strip()
    return ImageDescriptionResult(
        provider="openai:gpt-4.1-mini",
        description=description,
        raw_response=response.model_dump(),
    ).to_dict()
