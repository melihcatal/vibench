import json
from ibm_watsonx_ai.nlp import FoundationModelEndpointV2

def vendor_text_safety(text, api_key, project_id):
    """
    Moderate vendor notes using watsonx.ai guardrails.
    Returns (is_safe, flag_reason) tuple.
    """
    endpoint = FoundationModelEndpointV2(
        api_key=api_key,
        project_id=project_id,
        deployment_id="guardrails-deployment-id"
    )
    response = endpoint.analyze_content(text=text, task="moderation")
    result = response["moderation"]
    safe = result.get("is_safe", False)
    reason = result.get("flag_reason", "")
    return safe, reason
