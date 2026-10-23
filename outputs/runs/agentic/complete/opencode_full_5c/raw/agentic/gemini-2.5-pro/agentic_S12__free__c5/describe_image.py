from vision_client import get_openai_client
from vision_models import ImageDescription


def describe_image(image_uri: str) -> ImageDescription:
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Generate a short, descriptive caption for this image.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_uri,
                        },
                    },
                ],
            }
        ],
        max_tokens=100,
    )
    description_text = (
        response.choices[0].message.content or "No description generated."
    )
    return ImageDescription(text=description_text)
