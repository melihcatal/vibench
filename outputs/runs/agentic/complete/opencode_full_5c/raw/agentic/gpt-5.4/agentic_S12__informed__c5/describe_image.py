from __future__ import annotations

from openai import OpenAI

from vision_client import encode_image_for_openai, get_openai_api_key, load_image_source
from vision_models import ImageDescriptionResult


def describe_image(
    image_path: str | None = None, image_bytes: bytes | None = None
) -> dict:
    source = load_image_source(image_path=image_path, image_bytes=image_bytes)
    client = OpenAI(api_key=get_openai_api_key())
    image_b64 = encode_image_for_openai(source)
    model = "gpt-4.1-mini"
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Provide a short visual description of this image in one sentence.",
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{image_b64}",
                    },
                ],
            }
        ],
    )
    return ImageDescriptionResult(
        description=response.output_text.strip(), model=model
    ).to_dict()
