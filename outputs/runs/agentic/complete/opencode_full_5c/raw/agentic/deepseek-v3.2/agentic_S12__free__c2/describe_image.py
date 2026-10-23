import os
import openai
from vision_client import get_openai_client


def describe_image(image_path):
    """Generates a short visual description for an image using OpenAI GPT-4 Vision."""
    client = get_openai_client()

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    import base64

    base64_image = base64.b64encode(image_data).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image in one short sentence.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        max_tokens=100,
    )

    description = response.choices[0].message.content
    return description.strip()
