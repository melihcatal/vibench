from __future__ import annotations

from pathlib import Path

from vision_client import get_openai_vision_client, read_image_bytes
from vision_models import ImageDescriptionResult

MODEL_ID = "gpt-4o-mini"


def describe_image(image_path: str | Path, max_words: int = 25) -> ImageDescriptionResult:
    """Generate a short visual description using OpenAI GPT-4o mini vision."""
    client = get_openai_vision_client()
    image_bytes = read_image_bytes(image_path)
    description = client.responses.create(
        model=MODEL_ID,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": f"Describe this image in at most {max_words} words."},
                    {"type": "input_image", "image_url": f"data:image/jpeg;base64,{image_bytes.decode('latin1')}"},
                ],
            }
        ],
    )
    text = getattr(description, "output_text", "") or ""
    return ImageDescriptionResult(description=text.strip(), raw=description)
