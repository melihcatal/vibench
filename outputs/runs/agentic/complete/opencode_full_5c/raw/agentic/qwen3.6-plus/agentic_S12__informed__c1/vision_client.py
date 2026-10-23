import os
from typing import Optional


class VisionClientConfig:
    """Configuration for DashScope / Qwen-VL vision client."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "qwen-vl-max",
        base_url: str = "https://dashscope.aliyuncs.com/api/v1",
        timeout: int = 60,
        max_retries: int = 3,
    ):
        self.api_key = api_key or os.environ.get("DASHSCOPE_API_KEY", "")
        self.model = model
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

    def validate(self) -> None:
        if not self.api_key:
            raise ValueError(
                "DASHSCOPE_API_KEY environment variable is required for DashScope Qwen-VL"
            )


def create_vision_headers(api_key: str) -> dict:
    """Return HTTP headers for DashScope Qwen-VL API requests."""
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
    }


def build_vision_payload(
    model: str,
    image_url: str,
    prompt: str,
    max_tokens: int = 512,
    temperature: float = 0.1,
) -> dict:
    """Build a DashScope Qwen-VL multimodal request payload."""
    return {
        "model": model,
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"image": image_url},
                        {"text": prompt},
                    ],
                }
            ]
        },
        "parameters": {
            "max_tokens": max_tokens,
            "temperature": temperature,
        },
    }


def extract_text_from_response(response_json: dict) -> str:
    """Extract the assistant text from a DashScope Qwen-VL response."""
    choices = response_json.get("output", {}).get("choices", [])
    if choices:
        return choices[0].get("message", {}).get("content", "")
    return ""
