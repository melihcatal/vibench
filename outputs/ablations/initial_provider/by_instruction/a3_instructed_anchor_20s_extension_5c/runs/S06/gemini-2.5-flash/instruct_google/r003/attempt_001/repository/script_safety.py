from google.cloud import aiplatform
from google.cloud.aiplatform.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold

def check_script_safety(text: str) -> dict:
    """
    Checks narration scripts for unsafe content using Google Cloud Vertex AI and a generative model.
    """
    model = GenerativeModel("gemini-pro")

    # Define safety settings for the content generation (or analysis in this context)
    safety_settings = [
        {
            "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
            "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
    ]

    try:
        # For content safety, we'd typically analyze the input. 
        # Here, we'll pass the text and rely on the model's built-in safety filters
        # during content generation, which also apply to input analysis.
        response = model.generate_content(
            [text],
            safety_settings=safety_settings
        )
        
        # If the response is blocked, it means unsafe content was detected.
        # The API doesn't directly return a "safety score" for the input in this manner,
        # but rather blocks content that exceeds thresholds.
        # We can infer safety based on the presence of candidates.
        is_safe = bool(response.candidates)
        # A more detailed safety analysis would involve iterating through prompt_feedback.safety_ratings
        # if the model provides them directly for input (which Gemini does not in this direct call context for input only).
        # For this example, we'll simplify to a boolean based on content generation success.
        
        # Extract safety ratings if available (example structure, might need adjustment based on actual response)
        safety_ratings = []
        if response.prompt_feedback and response.prompt_feedback.safety_ratings:
            for rating in response.prompt_feedback.safety_ratings:
                safety_ratings.append({
                    "category": HarmCategory(rating.category).name,
                    "status": rating.probability_score # or a custom interpretation
                })

        return {
            "is_safe": is_safe,
            "status": "Content was not blocked by safety filters." if is_safe else "Content was blocked by safety filters.",
            "safety_ratings": safety_ratings,
            "provider": "Google Cloud Vertex AI (gemini-pro)"
        }
    except Exception as e:
        return {"is_safe": False, "status": f"Error during safety check: {str(e)}", "provider": "Google Cloud Vertex AI (gemini-pro)"}
