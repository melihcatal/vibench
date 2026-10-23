import json
from typing import Dict, Any
from model_models import ModelResponse

def platform_output_safety(response: ModelResponse) -> ModelResponse:
    """Check platform model output for unsafe content using watsonx.ai guardrails.

    Args:
        response: Raw model response containing 'output' and 'metadata'.

    Returns:
        A ModelResponse with a cleaned 'output' field and an added 'safety' field.
    """
    # watsonx.ai guardrails endpoint (provider-specific)
    from ibm_watsonx_ai import Guardrails
    guardrails = Guardrails(api_key=os.getenv("WATSONX_API_KEY"), project=os.getenv("WATSONX_PROJECT_ID"))
    unsafe = guardrails.check_content(response.output)
    cleaned = response.output if not unsafe else "[Content removed due to safety policy]"
    return ModelResponse(
        output=cleaned,
        metadata={**response.metadata, "safety": {
            "flagged": unsafe,
            "details": guardrails.get_details(),
        }},
    )
