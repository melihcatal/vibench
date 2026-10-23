import os
import requests
from typing import Dict, Any

# Example: Amazon Bedrock Guardrails (Text Content Safety)\n# Provider identification is visible via the endpoint URL

# ------------------------------------------------------------------\n# Configuration – set the required env vars before running\n# ------------------------------------------------------------------\nENDPOINT = os.getenv("AWS_CONTENT_SAFETY_ENDPOINT")
ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


def check_prompt_for_safety(prompt: str) -> Dict[str, Any]:
    """Runs the supplied prompt through Amazon Bedrock Guardrails and returns the report."""
    if not all([ENDPOINT, ACCESS_KEY, SECRET_KEY]):
        raise RuntimeError(
            "Environment variables AWS_CONTENT_SAFETY_ENDPOINT, "
            "AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY must be set."
        )

    payload = {
        "content": prompt,
        "config": {
            "rulesConfig": {
                "profile": "default",
                "riskLevels": ["high", "medium"],
            }
        },
    }

    headers = {
        "x-amz-api-name": "content-guard",
        "x-amz-target": "AWSContentGuardRuntimeApi.CheckContentSafety",
    }

    auth = (ACCESS_KEY, SECRET_KEY)
    response = requests.post(
        ENDPOINT,
        json=payload,
        headers=headers,
        auth=auth,
    )
    response.raise_for_status()
    return response.json()


def check_generated_text_for_safety(text: str) -> Dict[str, Any]:
    """Runs already‑generated text (e.g., LLM output) through the guardrails service."""
    payload = {
        "content": text,
        "config": {
            "rulesConfig": {
                "profile": "default",
                "riskLevels": ["high", "medium"],
            }
        },
    }
    headers = {
        "x-amz-api-name": "content-guard",
        "x-amz-target": "AWSContentGuardRuntimeApi.CheckContentSafety",
    }
    auth = (ACCESS_KEY, SECRET_KEY)
    resp = requests.post(ENDPOINT, json=payload, headers=headers, auth=auth)
    resp.raise_for_status()
    return resp.json()
