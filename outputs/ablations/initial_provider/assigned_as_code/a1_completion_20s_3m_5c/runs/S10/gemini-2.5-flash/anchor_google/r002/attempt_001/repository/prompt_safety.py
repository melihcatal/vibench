from typing import Dict, Any
from model_client import GeminiClient
from model_models import ModelPayload

def check_safety(payload: ModelPayload) -> Dict[str, Any]:
    client = GeminiClient()
    model = client.get_generative_model(model_name="gemini-pro")
    
    # Make a dummy call to get a response object with safety attributes
    # In a real scenario, you might integrate this check within a generation call
    response = model.generate_content(payload.text)
    
    safety_feedback = {
        "prompt_blocked": False,
        "safety_ratings": []
    }
    
    if response.prompt_feedback and response.prompt_feedback.block_reason:
        safety_feedback["prompt_blocked"] = True
        safety_feedback["block_reason"] = response.prompt_feedback.block_reason.name

    if response.candidates:
        # Check safety ratings for the generated content
        candidate = response.candidates[0]
        if candidate.finish_reason and candidate.finish_reason.name == "SAFETY":
            safety_feedback["generated_blocked"] = True
            safety_feedback["generated_block_reason"] = candidate.finish_reason.name

        if candidate.safety_ratings:
            for rating in candidate.safety_ratings:
                safety_feedback["safety_ratings"].append({
                    "category": rating.category.name,
                    "probability": rating.probability.name,
                    "blocked": rating.blocked
                })
    
    return safety_feedback
