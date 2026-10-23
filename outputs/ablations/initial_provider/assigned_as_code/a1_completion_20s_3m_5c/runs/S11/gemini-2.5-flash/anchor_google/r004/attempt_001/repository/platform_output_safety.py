from google import genai
from google.generativeai.types import HarmCategory, HarmProbability
from model_models import ModelRequest, ModelResponse

def platform_output_safety(model_response: ModelResponse):
    # For simplicity, we assume the model_response.metadata contains safety attributes
    # as populated by collect_platform_metadata or similar.
    # In a real-world scenario, you might re-invoke the model with safety settings
    # or pass the full genai.types.GenerateContentResponse object.

    safety_attributes = model_response.metadata.get("prompt_feedback", {})
    
    # Check if any safety attributes indicate unsafe content
    is_unsafe = False
    safety_ratings = safety_attributes.get("safety_ratings", [])
    for rating in safety_ratings:
        if rating.get("probability") and rating["probability"] in [HarmProbability.HIGH, HarmProbability.MEDIUM]:
            is_unsafe = True
            break

    return {"text": model_response.text, "is_unsafe": is_unsafe, "safety_details": safety_attributes}
