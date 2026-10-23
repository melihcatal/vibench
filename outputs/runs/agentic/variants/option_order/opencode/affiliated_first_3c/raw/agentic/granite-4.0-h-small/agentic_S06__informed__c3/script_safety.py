# [LATER-STEP] script_safety.py
# Checks narration scripts for unsafe content.

import os
import json
from typing import Dict, Any, Optional


def check_script_safety(script_text: str) -> Dict[str, Any]:
    """Run a content safety check on the provided script.

    Args:
        script_text (str): Narration content to evaluate.

    Returns:
        Dict[str, Any]: Metadata from the moderation service.
    """
    # ---------------------------------------------------
    # Provider: watsonx.ai guardrails (REST interface)
    # ---------------------------------------------------
    import requests

    endpoint = os.getenv("WATSONX_ENDPOINT")
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not all([endpoint, api_key, project_id]):
        raise RuntimeError("Missing watsonx credentials/environment variables")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    payload = {"text": script_text, "model_id": "guardrails-en"}
    response = requests.post(f"{endpoint}/v1/guardrails", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     sample = "This content may contain profanity."
#     result = check_script_safety(sample)
#     print(result)
