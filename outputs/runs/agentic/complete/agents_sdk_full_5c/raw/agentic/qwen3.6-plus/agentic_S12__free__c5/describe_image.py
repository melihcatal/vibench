"""
describe_image.py - Generates a short visual description for an image
using the OpenAI API with gpt-4o model for image understanding.
"""

from typing import Union
from pathlib import Path

from vision_client import (
    load_image_bytes,
    encode_image_base64,
    detect_image_mime,
    build_openai_client,
)
from vision_models import ImageDescription


def describe_image(
    image_source: Union[str, Path, bytes],
    max_tokens: int = 300,
    detail: str = "auto",
) -> ImageDescription:
    """
    Generate a visual description for an image using OpenAI's gpt-4o model.

    Args:
        image_source: Path to image file or raw image bytes.
        max_tokens: Maximum tokens for the response.
        detail: Level of detail for image analysis ("low", "high", or "auto").

    Returns:
        ImageDescription with the generated text.
    """
    client = build_openai_client()
    image_bytes = load_image_bytes(image_source)
    mime_type = detect_image_mime(image_bytes)
    base64_data = encode_image_base64(image_bytes)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a vision assistant. Describe the provided image in 2-3 concise sentences, focusing on key visual elements, subjects, and context.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_data}",
                            "detail": detail,
                        },
                    },
                    {
                        "type": "text",
                        "text": "Describe this image in 2-3 concise sentences.",
                    },
                ],
            },
        ],
        max_tokens=max_tokens,
    )

    description_text = response.choices[0].message.content or ""

    return ImageDescription(
        text=description_text.strip(),
        model_id="gpt-4o",
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        result = describe_image(image_path)
        print(f"Description ({result.model_id}): {result.text}")
