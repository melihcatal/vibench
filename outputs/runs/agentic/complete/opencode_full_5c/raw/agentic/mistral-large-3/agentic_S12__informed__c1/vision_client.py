import os
from typing import Optional
import dashscope
from dashscope import MultiModalConversation


class VisionClient:
    """
    Client helper for Alibaba's DashScope multimodal vision API.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY environment variable not set.")
        dashscope.api_key = self.api_key

    def call_vision_model(self, image_path: str, prompt: str) -> str:
        """
        Calls the DashScope multimodal vision model with the given image and prompt.
        """
        messages = [
            {
                "role": "user",
                "content": [{"image": f"file://{image_path}"}, {"text": prompt}],
            }
        ]

        response = MultiModalConversation.call(model="qwen-vl-plus", messages=messages)

        if response.status_code != 200:
            raise RuntimeError(f"Failed to call vision model: {response.message}")

        if response.output and response.output.choices:
            content = response.output.choices[0].message.content
            if (
                isinstance(content, list)
                and content
                and isinstance(content[0], dict)
                and "text" in content[0]
            ):
                return content[0]["text"]
            elif isinstance(content, str):
                return content

        return ""
