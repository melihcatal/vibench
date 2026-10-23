import os
import base64
import requests
from typing import Dict, Any


def describe_image(image_path: str) -> Dict[str, Any]:
    """
    Generates a short visual description for an image using OpenAI's GPT-4 Vision API.

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary containing the generated description
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image in one concise sentence.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 100,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    if response.status_code != 200:
        raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")

    data = response.json()
    description = data["choices"][0]["message"]["content"]

    return {
        "description": description.strip(),
        "model": "gpt-4-vision-preview",
        "usage": data.get("usage", {}),
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python describe_image.py <image_path>")
        sys.exit(1)

    try:
        result = describe_image(sys.argv[1])
        print(f"Description: {result['description']}")
        print(f"Model: {result['model']}")
    except Exception as e:
        print(f"Error: {e}")
