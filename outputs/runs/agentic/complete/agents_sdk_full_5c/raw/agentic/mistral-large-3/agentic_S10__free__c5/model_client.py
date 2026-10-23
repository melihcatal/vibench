import os
from typing import Optional
import httpx


def get_llm_client() -> httpx.Client:
    """
    Provide a configured HTTP client for Together.ai's hosted LLM API.
    """
    base_url = os.getenv("TOGETHER_API_BASE_URL", "https://api.together.xyz/v1")
    return httpx.Client(base_url=base_url, timeout=30.0)