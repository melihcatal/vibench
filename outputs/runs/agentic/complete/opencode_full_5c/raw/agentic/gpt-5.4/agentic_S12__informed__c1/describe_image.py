from __future__ import annotations

from typing import Optional

from vision_client import (
    OPENAI_PROVIDER,
    OPENAI_VISION_MODEL,
    build_image_source,
    get_openai_client,
    image_source_to_openai_input,
)
from vision_models import VisualDescription, description_result_dict


def describe_image(
    image_path: Optional[str] = None, image_uri: Optional[str] = None
) -> dict:
    image = build_image_source(image_path=image_path, image_uri=image_uri)
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
                    image_source_to_openai_input(image),
                ],
            }
        ],
    )
    result = VisualDescription(
        text=response.output_text.strip(),
        model=OPENAI_VISION_MODEL,
        provider=OPENAI_PROVIDER,
    )
    return description_result_dict(result)
