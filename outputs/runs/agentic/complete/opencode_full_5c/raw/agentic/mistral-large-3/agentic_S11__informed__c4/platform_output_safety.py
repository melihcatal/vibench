from typing import Dict, Any
import requests
import os


def platform_output_safety(text: str) -> Dict[str, Any]:
    """
    Checks watsonx.ai model output for unsafe content using watsonx.ai guardrails.
    Requires WATSONX_API_KEY and WATSONX_PROJECT_ID environment variables.
    """
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")

    if not api_key or not project_id:
        raise ValueError("WATSONX_API_KEY and WATSONX_PROJECT_ID must be set.")

    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation/hap_detection"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"project_id": project_id, "input": text}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()
    return {
        "is_safe": not result.get("results", [{}])[0].get("hap_present", False),
        "hap_score": result.get("results", [{}])[0].get("hap_score", 0.0),
        "provider": "watsonx.ai guardrails",
    }
