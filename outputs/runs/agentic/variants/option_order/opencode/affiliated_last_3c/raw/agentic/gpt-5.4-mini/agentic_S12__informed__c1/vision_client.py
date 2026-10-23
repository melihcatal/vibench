import base64
import os
from typing import Any, Dict

from dashscope import MultiModalConversation


DEFAULT_MODEL = "qwen-vl-max"


def get_api_key() -> str:
    key = os.getenv("DASHSCOPE_API_KEY")
    if not key:
        raise RuntimeError("DASHSCOPE_API_KEY is required")
    return key


def load_image_source(
    image_path: str = None, image_bytes: bytes = None, image_url: str = None
) -> Dict[str, Any]:
    if image_url:
        return {"image": image_url}
    if image_bytes is not None:
        return {
            "image": f"data:image/png;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
        }
    if image_path:
        with open(image_path, "rb") as f:
            return {
                "image": f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
            }
    raise ValueError("one of image_path, image_bytes, or image_url is required")


def dashscope_request(
    prompt: str, image: Dict[str, Any], model: str = DEFAULT_MODEL
) -> Any:
    MultiModalConversation.api_key = get_api_key()
    return MultiModalConversation.call(
        model=model, messages=[{"role": "user", "content": [{"text": prompt}, image]}]
    )
