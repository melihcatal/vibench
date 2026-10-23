import os
import requests
from typing import Dict, Any, Tuple


def check_prompt_safety(
    text: str, api_key: str = None, endpoint: str = "https://api.tisane.ai/v1/moderate"
) -> Tuple[bool, Dict[str, Any]]:
    """
    Checks if the provided text contains unsafe content using the Tisane API.

    Args:
        text: Input text to check for unsafe content.
        api_key: Tisane API key. Defaults to TISANE_API_KEY environment variable.
        endpoint: Tisane API endpoint.

    Returns:
        A tuple containing:
        - bool: True if the text is safe, False otherwise.
        - dict: Detailed moderation results.
    """
    api_key = api_key or os.getenv("TISANE_API_KEY")
    if not api_key:
        raise ValueError("TISANE_API_KEY environment variable not set")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "text": text,
        "settings": {"checks": ["hate", "violence", "sexual", "bullying", "self_harm"]},
    }

    response = requests.post(endpoint, json=payload, headers=headers)
    response.raise_for_status()

    result = response.json()
    is_safe = not any(
        result.get("moderation", {}).get(check, {}).get("flagged", False)
        for check in ["hate", "violence", "sexual", "bullying", "self_harm"]
    )

    return is_safe, result
