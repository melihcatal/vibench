"""
Generate a short visual description for an image using OpenAI GPT-4 Vision.
Provider: OpenAI (api.openai.com) - gpt-4o model
"""

from typing import Optional

from vision_client import get_openai_client, load_image_bytes, get_mime_type, encode_image_to_base64_url
from vision_models import ImageDescription, ImageAnalysisPayload


DEFAULT_DESCRIPTION_PROMPT = (
    "Provide a concise, accurate description of this image. "
    "Focus on the main subjects, setting, and notable visual details. "
    "Keep the description to 2-4 sentences."
)


def describe_image(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    prompt: str = DEFAULT_DESCRIPTION_PROMPT,
    model: str = "gpt-4o",
    max_tokens: int = 300,
    detail: str = "auto",
) -> ImageAnalysisPayload:
    """
    Generate a visual description for a static image using OpenAI GPT-4 Vision.

    Uses the OpenAI Chat Completions API with vision support (gpt-4o model)
    to produce natural language descriptions of image content.

    Args:
        image_path: Path to the image file.
        image_bytes: Raw image bytes.
        prompt: Custom prompt for the description task.
        model: OpenAI model identifier (default: gpt-4o).
        max_tokens: Maximum tokens for the response.
        detail: Image detail level ('low', 'high', 'auto').

    Returns:
        ImageAnalysisPayload containing the generated description.
    """
    raw_image = load_image_bytes(image_path=image_path, image_bytes=image_bytes)
    mime_type = get_mime_type(image_path) if image_path else "image/jpeg"
    data_url = encode_image_to_base64_url(raw_image, mime_type)

    client = get_openai_client()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a visual analysis assistant that provides clear, concise image descriptions."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": data_url,
                            "detail": detail,
                        },
                    },
                ],
            },
        ],
        max_tokens=max_tokens,
    )

    description = ImageDescription.from_openai_response(response)

    payload = ImageAnalysisPayload(
        image_path=image_path,
        description=description,
        metadata={
            "provider": "openai_vision",
            "vision_model": model,
            "vision_model_family": "gpt-4o",
            "prompt_tokens": description.prompt_tokens,
            "completion_tokens": description.completion_tokens,
            "openai_endpoint": "https://api.openai.com/v1",
        },
    )

    return payload


def describe_image_with_context(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    context: str = "",
    model: str = "gpt-4o",
) -> ImageAnalysisPayload:
    """
    Generate a visual description with additional context or domain-specific guidance.

    Args:
        image_path: Path to the image file.
        image_bytes: Raw image bytes.
        context: Additional context to guide the description.
        model: OpenAI model identifier.

    Returns:
        ImageAnalysisPayload with the contextualized description.
    """
    contextual_prompt = (
        f"{DEFAULT_DESCRIPTION_PROMPT}\n\n"
        f"Additional context: {context}\n\n"
        f"Please incorporate this context into your description."
    )

    return describe_image(
        image_path=image_path,
        image_bytes=image_bytes,
        prompt=contextual_prompt,
        model=model,
    )


def generate_alt_text(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    model: str = "gpt-4o",
) -> str:
    """
    Generate accessibility-friendly alt text for an image.

    Args:
        image_path: Path to the image file.
        image_bytes: Raw image bytes.
        model: OpenAI model identifier.

    Returns:
        Alt text string suitable for web accessibility.
    """
    alt_prompt = (
        "Write concise, descriptive alt text for this image suitable for web accessibility. "
        "Focus on the essential visual information a sighted user would get from the image. "
        "Keep it under 125 characters. Start directly with the description."
    )

    payload = describe_image(
        image_path=image_path,
        image_bytes=image_bytes,
        prompt=alt_prompt,
        model=model,
        max_tokens=150,
    )

    return payload.description.text if payload.description else ""


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = describe_image(image_path=sys.argv[1])
        if result.description:
            print(result.description.text)
