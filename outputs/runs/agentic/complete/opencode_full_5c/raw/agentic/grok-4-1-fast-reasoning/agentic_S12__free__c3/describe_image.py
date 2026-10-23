from openai import OpenAI
from vision_client import image_to_base64
from vision_models import ImageDescription


def describe_image(image_path: str) -> ImageDescription:
    client = OpenAI()
    base64_image = image_to_base64(image_path)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Provide a short 1-2 sentence visual description of this image.",
                    },
                    {"type": "image_url", "image_url": {"url": base64_image}},
                ],
            },
        ],
        max_tokens=100,
    )
    desc = response.choices[0].message.content.strip()
    return ImageDescription(description=desc)
