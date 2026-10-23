import os
import requests
from model_models import LLMResponse


def check_prompt_safety(text: str) -> bool:
    """Checks a prompt or generated text for unsafe content using Watsonx Guardrails API.

    Returns True if safe, False otherwise.
    """
    endpoint = os.getenv(
        "WATSONX_GUARD_ENDPOINT", "https://api.watsonx.ibm.com/v1/guardrails"
    )
    api_key = os.getenv("WATSONX_API_KEY")
    if not api_key:
        raise RuntimeError("WATSONX_API_KEY environment variable not set")

    payload = {
        "input": {"text": text},
        "guardrails": {"high_risk_content_detection": {}},
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    response = requests.post(endpoint, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    # Example structure: {"result": {"high_risk_content_detection": {"safe": true}}}
    safe = (
        result.get("result", {})
        .get("high_risk_content_detection", {})
        .get("safe", False)
    )
    return safe
