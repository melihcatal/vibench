import os
from typing import Optional
import dashscope
from dashscope import MultiModalConversation
from .vision_models import ImageDescriptionResponse


def describe_image(
    image_path: str, api_key: Optional[str] = None
) -> ImageDescriptionResponse:
    """
    Generates a short visual description for an image using Alibaba's Qwen-VL model via DashScope.
    """
    api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set.")

    dashscope.api_key = api_key

    messages = [
        {
            "role": "user",
            "content": [
                {"image": f"file://{image_path}"},
                {
                    "text": "Provide a concise and accurate description of this image in one sentence."
                },
            ],
        }
    ]

    response = MultiModalConversation.call(model="qwen-vl-plus", messages=messages)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to describe image: {response.message}")

    description = ""
    if response.output and response.output.choices:
        content = response.output.choices[0].message.content
        if (
            isinstance(content, list)
            and content
            and isinstance(content[0], dict)
            and "text" in content[0]
        ):
            description = content[0]["text"]
        elif isinstance(content, str):
            description = content

    return ImageDescriptionResponse(description=description)
