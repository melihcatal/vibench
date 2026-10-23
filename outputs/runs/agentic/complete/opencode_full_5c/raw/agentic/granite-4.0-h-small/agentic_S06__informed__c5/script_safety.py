import os
from ibm_watsonx_ai import WatsonxAiService
from ibm_watsonx_ai.auth import IamParam

# Authenticate to watsonx.ai Guardrails using environment variables
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
authenticator = IamParam(apikey=WATSONX_API_KEY)
service = WatsonxAiService(resource_instance_id=PROJECT_ID, authenticator=authenticator)


def check_script_for_unsafe_content(script: str) -> dict:
    """Run watsonx.ai Guardrails / HAP detection on a narration script.

    Args:
        script (str): The script content.

    Returns:
        dict: Guardrails response containing safety scores and flagged categories.
    """
    response = service.ai_content_guardrails(
        content=script, content_type="text/plain", purpose="text"
    ).get_result()
    return response


def is_script_safe(script: str, threshold: float = 0.05) -> bool:
    """Simple wrapper to decide whether a script is safe.

    Args:
        script (str): Input script.
        threshold (float): Acceptable risk (default 0.05 = 5%).

    Returns:
        bool: True if risk score below threshold, else False.
    """
    resp = check_script_for_unsafe_content(script)
    # Example response field: risk_score (float), categories list
    if resp.get("risk_score", 0.0) < threshold:
        return True
    return False
