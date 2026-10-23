# [LATER-STEP] script_safety.py
# Check narration scripts for unsafe content using watsonx.ai Guardrails

import json
from ibm_watsonx_ai.services import RiskDetection
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os


def check_script_safety(script: str) -> bool:
    """Run the script through watsonx guardrails and return safety flag.

    Args:
        script (str): Narration script.

    Returns:
        bool: True if safe, False otherwise.
    """
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    if not api_key or not project_id:
        raise RuntimeError("WATSONX_API_KEY or WATSONX_PROJECT_ID not configured")
    authenticator = IAMAuthenticator(api_key)
    client = RiskDetection(
        authenticator=authenticator, service_url="https://api.watsonx.ibm.com"
    )
    response = client.run_analysis(text=script).get_result()
    # Simplified check: if any risk type is flagged, consider unsafe
    risks = response.get("risks", [])
    return not risks
