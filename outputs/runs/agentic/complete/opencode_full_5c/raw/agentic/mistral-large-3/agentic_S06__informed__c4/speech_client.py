import os
import dashscope
from dashscope.audio.tts import CosyVoice
from dashscope.common.api_identity import ApiIdentity
from typing import Optional


def get_client() -> CosyVoice:
    """Initialize and return a DashScope CosyVoice client."""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")

    identity = ApiIdentity(api_key=api_key)
    dashscope.api_identity = identity
    return CosyVoice()


def get_model_config(model: str = "CosyVoice-300M-SFT") -> dict:
    """Return configuration for the specified model."""
    return {"model": model, "response_format": "wav"}
