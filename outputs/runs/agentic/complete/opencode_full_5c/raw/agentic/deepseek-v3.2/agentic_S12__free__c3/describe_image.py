import os
import base64
from typing import Dict, Any
import requests
from vision_client import get_openai_api_key


def describe_image(image_path: str) -> Dict[str, Any]:
    """
    Generate a short visual description for an image using OpenAI's GPT-4 Vision API.

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary containing the generated description
    """
    api_key = get_openai_api_key()

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    base64_image = base64.b64encode(image_data).decode("utf-8")

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image in one or two sentences.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )
    response.raise_for_status()

    result = response.json()

    return {
        "description": result["choices"][0]["message"]["content"],
        "model": "gpt-4-vision-preview",
        "usage": result.get("usage", {}),
    }
