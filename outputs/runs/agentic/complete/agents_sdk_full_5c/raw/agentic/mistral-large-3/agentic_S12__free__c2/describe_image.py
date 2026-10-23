import base64
import os
import requests
from vision_models import ImageDescriptionResponse

def describe_image(image_path: str) -> ImageDescriptionResponse:
    """Generates a short visual description for an image using OpenAI's GPT-4 Vision API."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image in one sentence."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    
    description = response.json()["choices"][0]["message"]["content"]
    return ImageDescriptionResponse(
        provider="openai_gpt4_vision",
        description=description
    )