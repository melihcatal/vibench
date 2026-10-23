import os

# Provider: DashScope Qwen API (placeholder for LLM inference)

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


def create_chat_client() -> object:
    """Create and return a DashScope chat client with the configured API key."""
    if not DASHSCOPE_API_KEY:
        raise ValueError("Set DASHSCOPE_API_KEY environment variable")
    return dashscope.TextChat(api_key=DASHSCOPE_API_KEY)
