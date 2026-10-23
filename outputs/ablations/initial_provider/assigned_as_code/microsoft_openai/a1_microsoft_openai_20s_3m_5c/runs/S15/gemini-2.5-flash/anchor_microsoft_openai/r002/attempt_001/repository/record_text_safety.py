from vertexai.preview.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold
import os


def record_text_safety(text_content: str) -> dict:
    model = GenerativeModel("gemini-pro") # Using gemini-pro for content analysis as well
    
    # Configure safety settings to get a detailed breakdown, not just blocking
    # We set thresholds to BLOCK_NONE to get scores for all categories
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    response = model.generate_content(
        text_content,
        safety_settings=safety_settings
    )
    
    # The safety attributes are usually in the candidates[0].safety_ratings
    safety_ratings = []
    if response.candidates and response.candidates[0].safety_ratings:
        for rating in response.candidates[0].safety_ratings:
            safety_ratings.append({
                "category": rating.category.name,
                "probability": rating.probability.name,
                "blocked": rating.blocked
            })

    return {"safety_ratings": safety_ratings}
