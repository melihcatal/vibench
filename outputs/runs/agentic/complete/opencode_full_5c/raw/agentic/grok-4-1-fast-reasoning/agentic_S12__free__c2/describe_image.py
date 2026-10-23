import os
from openai import OpenAI
import vision_client


def describe_image(image_path: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    base64_image = vision_client.get_base64_image(image_path)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Generate a short one-sentence visual description of this image.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
        ],
        max_tokens=50,
    )
    return response.choices[0].message.content.strip()
