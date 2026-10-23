from __future__ import annotations

from typing import Optional

from vision_client import (
    OPENAI_PROVIDER,
    OPENAI_VISION_MODEL,
    build_openai_image_input,
    get_openai_client,
)
from vision_models import ImageDescriptionResult


def describe_image(
    image_path: Optional[str] = None, image_uri: Optional[str] = None
) -> dict:
    client = get_openai_client()
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
                    build_openai_image_input(
                        image_path=image_path, image_uri=image_uri
                    ),
                ],
            }
        ],
    )
    result = ImageDescriptionResult(
        provider=OPENAI_PROVIDER,
        description=response.output_text.strip(),
        model=OPENAI_VISION_MODEL,
        raw_response={"id": response.id},
    )
    return result.to_dict()
