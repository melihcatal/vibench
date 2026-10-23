import os
from openai import OpenAI


def get_vision_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.openai.com/v1",
    )
    return client


VISION_MODEL = "gpt-4o"


def build_vision_payload(image_url=None, image_base64=None, prompt=None):
    content = []
    if image_url:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": image_url},
            }
        )
    elif image_base64:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
            }
        )
    if prompt:
        content.append(
            {
                "type": "text",
                "text": prompt,
            }
        )
    return {
        "model": VISION_MODEL,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 1024,
    }


def parse_vision_response(response):
    if response and response.choices:
        return response.choices[0].message.content.strip()
    return ""
