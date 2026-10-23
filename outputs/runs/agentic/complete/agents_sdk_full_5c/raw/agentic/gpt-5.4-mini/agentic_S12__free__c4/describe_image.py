from __future__ import annotations

from vision_client import get_openai_vision_client
from vision_models import ImageDescriptionRequest, normalize_description


def describe_image(image_url: str, *, image_path: str | None = None, max_tokens: int = 80) -> str:
    """Generate a short visual description for an image using OpenAI GPT-4o vision."""
    request = ImageDescriptionRequest(image_url=image_url, image_path=image_path, max_tokens=max_tokens)
    client = get_openai_vision_client()
    response = client.describe_image(request)
    return normalize_description(response)
