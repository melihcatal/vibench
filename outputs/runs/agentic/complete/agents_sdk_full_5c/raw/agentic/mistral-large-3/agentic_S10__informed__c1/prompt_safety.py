import os
import requests
from typing import Dict, Any


def check_prompt_safety(
    text: str,
    api_key: Optional[str] = None,
    endpoint: str = "https://api.us-south.ai.content-safety.cloud.ibm.com/instances/"
) -> Dict[str, Any]:
    """
    Check prompts and generated text for unsafe content using watsonx.ai HAP detection.
    """
    api_key = api_key or os.getenv("WATSONX_API_KEY")
    instance_id = os.getenv("WATSONX_CONTENT_SAFETY_INSTANCE_ID")
    if not api_key or not instance_id:
        raise ValueError("WATSONX_API_KEY and WATSONX_CONTENT_SAFETY_INSTANCE_ID must be set")

    url = f"{endpoint}{instance_id}/v1/text/hap-detection"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {"text": text}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()