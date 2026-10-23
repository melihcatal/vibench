import os
from openai import OpenAI
from vision_client import image_to_base64
from vision_models import VisionDescription


def describe_image(image_path: str) -> VisionDescription:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    base64_image = image_to_base64(image_path)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Provide a short one-sentence description of the image.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        max_tokens=50,
    )
    description = response.choices[0].message.content.strip()
    return VisionDescription(description=description)
