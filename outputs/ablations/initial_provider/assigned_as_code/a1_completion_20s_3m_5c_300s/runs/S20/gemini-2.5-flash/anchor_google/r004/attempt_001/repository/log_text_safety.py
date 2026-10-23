from observability_client import ObservabilityClient
from observability_models import TextSafetyRequest
from vertexai.preview.generative_models import HarmCategory, HarmBlockThreshold

def check_log_text_safety(project_id: str, text_content: str):
    client = ObservabilityClient(project_id=project_id)

    # The generate_content method implicitly performs safety checks and returns safety attributes.
    # We need to explicitly configure the safety settings for a more direct check.
    # Vertex AI GenerativeModel's generate_content method has a `safety_settings` parameter.

    # Example of safety settings (adjust thresholds as needed)
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }

    response = client.generative_model.generate_content(text_content, safety_settings=safety_settings)

    # The response object will contain `prompt_feedback` and `candidates` with `safety_ratings`
    # if there are any issues.
    safety_attributes = {
        "blocked": False,
        "harm_categories": []
    }

    if response.prompt_feedback and response.prompt_feedback.block_reason:
        safety_attributes["blocked"] = True
        safety_attributes["block_reason"] = str(response.prompt_feedback.block_reason)
    
    if response.candidates:
        for candidate in response.candidates:
            if candidate.safety_ratings:
                for rating in candidate.safety_ratings:
                    if rating.blocked:
                        safety_attributes["blocked"] = True
                        safety_attributes["harm_categories"].append({
                            "category": str(rating.category),
                            "probability": str(rating.probability),
                        })
    
    return {"safety_attributes": safety_attributes}
