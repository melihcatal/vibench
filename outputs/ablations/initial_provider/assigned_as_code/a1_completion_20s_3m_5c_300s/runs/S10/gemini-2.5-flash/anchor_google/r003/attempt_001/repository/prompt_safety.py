import os
from typing import Any, Dict, List
import google.generativeai as genai
from model_client import GeminiClient

def prompt_safety(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    client = GeminiClient(api_key=config.get("api_key"))
    model = client.get_model("gemini-1.5-flash")

    text_to_check = payload.get("text", "")
    if not text_to_check:
        raise ValueError("Payload must contain 'text' for safety check.")

    # Using generate_content to leverage built-in safety features
    # The actual generated content is not important, we care about the safety ratings
    response = model.generate_content(text_to_check)

    safety_feedback = {
        "prompt_feedback": [],
        "candidate_safety_ratings": []
    }

    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        for rating in response.prompt_feedback.safety_ratings:
            safety_feedback["prompt_feedback"].append({
                "category": str(rating.category).split('.')[-1],
                "probability": str(rating.probability).split('.')[-1]
            })

    if response.candidates and response.candidates[0].safety_ratings:
        for rating in response.candidates[0].safety_ratings:
            safety_feedback["candidate_safety_ratings"].append({
                "category": str(rating.category).split('.')[-1],
                "probability": str(rating.probability).split('.')[-1]
            })

    return safety_feedback
