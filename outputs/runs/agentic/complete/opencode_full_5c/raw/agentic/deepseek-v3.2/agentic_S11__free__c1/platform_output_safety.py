import os
from typing import Dict, Any
import google.generativeai as genai
from model_models import PlatformResponse


def check_platform_output_safety(response: PlatformResponse) -> Dict[str, Any]:
    """Check platform model output for unsafe content using Google's safety API."""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")

    safety_prompt = f"""
    Analyze the following text for safety concerns. Return a JSON with:
    - "is_safe": boolean
    - "categories": list of unsafe categories found (if any)
    - "confidence": float between 0 and 1
    - "reason": brief explanation
    
    Text to analyze: {response.content[:1000]}
    """

    try:
        safety_response = model.generate_content(
            safety_prompt,
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
            ],
        )

        result = {
            "provider": "google_generative_ai",
            "model_used": "gemini-pro",
            "original_model": response.model_id,
            "safety_check": "completed",
        }

        if safety_response.prompt_feedback:
            result["block_reason"] = safety_response.prompt_feedback.block_reason
            result["safety_ratings"] = [
                {
                    "category": rating.category.name,
                    "probability": rating.probability.name,
                }
                for rating in safety_response.prompt_feedback.safety_ratings
            ]

        return result

    except Exception as e:
        return {
            "provider": "google_generative_ai",
            "model_used": "gemini-pro",
            "original_model": response.model_id,
            "safety_check": "failed",
            "error": str(e),
        }
