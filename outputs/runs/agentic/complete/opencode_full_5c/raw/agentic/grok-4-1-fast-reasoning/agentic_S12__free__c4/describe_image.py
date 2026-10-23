import base64
import os
from openai import OpenAI
from vision_client import OPENAI_API_KEY, image_b64


def describe_image(image_path: str) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)
    b64str = image_b64(image_path)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Generate a short visual description for this image in one sentence.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64str}"},
                    },
                ],
            }
        ],
        max_tokens=100,
    )
    return response.choices[0].message.content
