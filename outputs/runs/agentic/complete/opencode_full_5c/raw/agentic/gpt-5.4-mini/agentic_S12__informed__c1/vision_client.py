import os
from typing import Any

from dashscope import MultiModalConversation


DEFAULT_VISION_MODEL = "qwen-vl-max"


def get_dashscope_api_key() -> str:
    key = os.getenv("DASHSCOPE_API_KEY", "")
    if not key:
        raise RuntimeError("DASHSCOPE_API_KEY is required")
    return key


def make_dashscope_client() -> Any:
    return MultiModalConversation


def vision_model_name() -> str:
    return os.getenv("DASHSCOPE_VISION_MODEL", DEFAULT_VISION_MODEL)
