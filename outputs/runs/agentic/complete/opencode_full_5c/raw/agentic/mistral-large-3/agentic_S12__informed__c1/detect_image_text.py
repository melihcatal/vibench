import os
from typing import List, Optional
import dashscope
from dashscope import MultiModalConversation
from .vision_models import TextDetectionResponse


def detect_image_text(
    image_path: str, api_key: Optional[str] = None
) -> TextDetectionResponse:
    """
    Detects text appearing inside an image using Alibaba's Qwen-VL model via DashScope.
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
                    "text": "Extract all visible text from this image. Return only the text as a list of strings, one for each line or distinct text block."
                },
            ],
        }
    ]

    response = MultiModalConversation.call(model="qwen-vl-plus", messages=messages)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to detect text: {response.message}")

    texts = []
    if response.output and response.output.choices:
        content = response.output.choices[0].message.content
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and "text" in item:
                    texts.extend(
                        [
                            text.strip()
                            for text in item["text"].split("\n")
                            if text.strip()
                        ]
                    )
        elif isinstance(content, str):
            texts.extend([text.strip() for text in content.split("\n") if text.strip()])

    return TextDetectionResponse(texts=texts)
