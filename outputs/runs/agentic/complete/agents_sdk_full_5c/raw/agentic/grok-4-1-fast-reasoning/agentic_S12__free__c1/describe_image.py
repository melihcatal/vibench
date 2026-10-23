from openai import OpenAI
import os
from vision_client import load_image_bytes, image_to_base64
from vision_models import ImageDescription

def describe_image(image_path: str) -> ImageDescription:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    image_bytes = load_image_bytes(image_path)
    base64_image = image_to_base64(image_bytes)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Provide a short one-sentence description of the main content of this image."
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": base64_image}
                    }
                ]
            }
        ],
        max_tokens=100
    )
    description = response.choices[0].message.content.strip()
    return ImageDescription(description=description)