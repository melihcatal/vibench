# [LATER-STEP] platform_output_safety.py

import json
from model_models import ManagedModelResponse

# Example: using watsonx guardrails SDK (sdk=ibm-watsonx-ai) – guardrails interface
# For the purpose of this illustration we import the guardrails client and assume it exists.
# Adjust import / client class according to the actual package name/version.
# from ibm_watsonx_ai.guardrails import GuardrailsClient


def detect_unsafe_content(response: ManagedModelResponse) -> ManagedModelResponse:
    """Check platform model output for unsafe content using a guardrails service.

    Args:
        response (ManagedModelResponse): Response with raw provider payload.

    Returns:
        ManagedModelResponse: Same object enriched with a 'safety_check' metadata field.
    """
    # Placeholder for actual guardrails client initialization
    # guardrails = GuardrailsClient(api_key=os.getenv('WATSONX_API_KEY'), project_id=os.getenv('WATSONX_PROJECT_ID'))
    # guardrails_result = guardrails.analyze_content(response.provider_payload['content'])

    # Simulated guardrails decision (True = unsafe)
    unsafe = False  # guardrails_result.get('unsafe', False)

    enriched = response.copy()
    enriched["metadata"]["safety_check"] = {
        "unsafe": unsafe,
        "details": "Placeholder – watsonx guardrails result",
    }
    return enriched
