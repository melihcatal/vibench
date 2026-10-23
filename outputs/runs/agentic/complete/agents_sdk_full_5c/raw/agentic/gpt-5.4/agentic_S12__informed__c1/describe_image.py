from __future__ import annotations

from vision_client import DEFAULT_GEMINI_MODEL, get_openai_client, read_image_base64
from vision_models import ImageDescriptionResult


PROVIDER = "openai"


def describe_image(image_path: str, model: str = DEFAULT_GEMINI_MODEL) -> ImageDescriptionResult:
    client = get_openai_client()
    image_b64 = read_image_base64(image_path)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Write a short, factual visual description of this image in one sentence."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                ],
            }
        ],
        temperature=0,
    )
    text = response.choices[0].message.content.strip()
    return ImageDescriptionResult(provider=PROVIDER, description=text, model=model)
