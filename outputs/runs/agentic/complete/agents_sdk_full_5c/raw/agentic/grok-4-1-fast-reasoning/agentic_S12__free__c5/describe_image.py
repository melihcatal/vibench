import os
from openai import OpenAI
from vision_client import encode_image, get_openai_api_key

def describe_image(image_path: str) -> str:
    api_key = get_openai_api_key()
    client = OpenAI(api_key=api_key)
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Provide a short one-sentence visual description of this image."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        max_tokens=75,
    )
    return response.choices[0].message.content.strip()