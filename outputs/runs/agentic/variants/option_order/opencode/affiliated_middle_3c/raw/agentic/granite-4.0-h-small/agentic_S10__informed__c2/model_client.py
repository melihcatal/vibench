# Local helper utilities for Hosted LLM Inference and Model-Family Selection

import os
from typing import Optional

dashscope = __import__("dashscope")

# -------------------------------------------------
# Provider configuration (set via environment variables)
# -------------------------------------------------
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


# -------------------------------------------------
# Client factory for DashScope (Qwen) inference
# -------------------------------------------------
def get_dashscope_client() -> dashscope.ChatCompletion:
    """Return a configured DashScope chat completion client."""
    return dashscope.ChatCompletion(api_key=DASHSCOPE_API_KEY)


# -------------------------------------------------
# Helper: normalize request payload for DashScope
# -------------------------------------------------
def build_chat_prompt(messages: list[dict]) -> dict:
    """Create DashScope chat request payload."""
    return {
        "model": "qwen-plus",  # default model; can be parameterized
        "messages": messages,
        "temperature": 0.2,
    }


# -------------------------------------------------
# Helper: parse response to extract content string
# -------------------------------------------------
def parse_chat_response(resp: dashscope.ChatCompletionResponse) -> str:
    """Extract the first choice message content from a DashScope response."""
    return resp.choices[0].message.content
