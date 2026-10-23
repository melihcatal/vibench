from anthropic import Anthropic
from vision_client import get_anthropic_api_key

def image_summary(labels: list, description: str, texts: list, safety: dict) -> str:
    api_key = get_anthropic_api_key()
    client = Anthropic(api_key=api_key)
    prompt = f"""Summarize these image analysis results in 1-2 sentences:

Labels/Objects: {labels}
Description: {description}
Detected Text: {texts}
Safety Assessment: {safety}"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()