import os
from typing import List, Dict, Any

import google.generativeai as genai

from observability_client import get_gemini_model


def check_log_text_safety(log_message: str) -> Dict[str, Any]:
    model = get_gemini_model("gemini-pro") # Using gemini-pro for content safety analysis

    # The Gemini API has built-in safety features. When generating content,
    # you can inspect the `prompt_feedback` and `candidates[0].safety_ratings`
    # for safety information.
    # For a direct safety check, we can try to generate content and observe feedback.
    # However, a more explicit safety check might involve asking the model to evaluate.

    prompt = f"Analyze the following log message for any unsafe, harmful, or sensitive content and provide a safety report: {log_message}"

    try:
        response = model.generate_content(prompt,
            safety_settings={
                genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
            }
        )

        safety_attributes = {
            "analyzed_message": log_message,
            "summary": response.text, # The model's direct assessment
            "safety_ratings": []
        }

        # If the response has safety ratings, include them
        if hasattr(response, 'prompt_feedback') and response.prompt_feedback.safety_ratings:
            for rating in response.prompt_feedback.safety_ratings:
                safety_attributes["safety_ratings"].append({
                    "category": str(rating.category).split('.')[-1],
                    "probability": str(rating.probability).split('.')[-1]
                })
        elif hasattr(response, 'candidates') and response.candidates:
             if hasattr(response.candidates[0], 'safety_ratings') and response.candidates[0].safety_ratings:
                for rating in response.candidates[0].safety_ratings:
                    safety_attributes["safety_ratings"].append({
                        "category": str(rating.category).split('.')[-1],
                        "probability": str(rating.probability).split('.')[-1]
                    })


        return safety_attributes

    except Exception as e:
        return {"error": f"Error checking safety: {e}", "message": log_message}
