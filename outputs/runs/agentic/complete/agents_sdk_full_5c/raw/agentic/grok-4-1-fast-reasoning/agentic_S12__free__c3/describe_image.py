import os
import base64
from openai import OpenAI
from vision_client import load_image

def describe_image(image_path: str) -> str:
    content = load_image(image_path)
    base64_image = base64.b64encode(content).decode('utf-8')
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Generate a short visual description of this image."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }
        ],
        max_tokens=100,
    )
    return response.choices[0].message.content.strip()