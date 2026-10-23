import os
from typing import List, Dict, Optional
import dashscope
from dashscope import MultiModalConversation
from .vision_models import (
    LabelDetectionResponse,
    ImageDescriptionResponse,
    TextDetectionResponse,
    SafetyScoreResponse,
)


def detect_image_labels(
    image_path: str, api_key: Optional[str] = None
) -> LabelDetectionResponse:
    """
    Detects labels or objects in a static image using Alibaba's Qwen-VL model via DashScope.
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
                    "text": "Identify and list all objects and labels in this image. Return only the labels as a list of strings."
                },
            ],
        }
    ]

    response = MultiModalConversation.call(model="qwen-vl-plus", messages=messages)

    if response.status_code != 200:
        raise RuntimeError(f"Failed to detect labels: {response.message}")

    labels = []
    if response.output and response.output.choices:
        content = response.output.choices[0].message.content
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and "text" in item:
                    labels.extend(
                        [
                            label.strip()
                            for label in item["text"].split(",")
                            if label.strip()
                        ]
                    )
        elif isinstance(content, str):
            labels.extend(
                [label.strip() for label in content.split(",") if label.strip()]
            )

    return LabelDetectionResponse(labels=labels)
