from google import genai
from model_models import ModelInvocationPayload, ModelConfig, SafetyCheckResponse
from model_client import get_vertex_ai_client
from typing import List

def check_platform_output_safety(
    payload: ModelInvocationPayload, config: ModelConfig
) -> SafetyCheckResponse:
    client = get_vertex_ai_client(config.project_id, config.location)
    model = client.get_model(config.model_id)

    # Note: For safety attributes, often the input is also checked. 
    # Here we are focusing on output safety check after generation.
    response = model.generate_content(
        payload.text
    )

    is_safe = True
    reasons: List[str] = []

    if response.candidates:
        for candidate in response.candidates:
            if candidate.safety_ratings:
                for rating in candidate.safety_ratings:
                    # Assuming Block_NONE means safe, anything else means potentially unsafe
                    if rating.blocked: # or rating.probability > 0.5 for example to set a threshold
                        is_safe = False
                        reasons.append(f"Category: {rating.category.name}, Blocked: {rating.blocked}, Probability: {rating.probability.name}")
            # Also check finish_reason for SAFETY as a blocking reason
            if candidate.finish_reason and candidate.finish_reason.name == "SAFETY":
                is_safe = False
                reasons.append(f"Generation stopped due to safety concerns.")

    return SafetyCheckResponse(is_safe=is_safe, reasons=reasons)
