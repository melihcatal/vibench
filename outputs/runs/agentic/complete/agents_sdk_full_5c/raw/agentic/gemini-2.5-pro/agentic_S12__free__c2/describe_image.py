import os
import base64
import openai
from vision_models import ImageDescription

def describe_image(image_bytes: bytes) -> ImageDescription:
    """
    Generates a short visual description for an image using OpenAI's GPT-4o model.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Generate a short, one-sentence description for this image."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                ],
            }
        ],
        max_tokens=100,
    )
    
    description_text = response.choices[0].message.content if response.choices else "No description generated."
    return ImageDescription(text=description_text)
