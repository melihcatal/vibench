import os
import google.generativeai as genai

def check_safety(text: str):
    """
    Checks the given text for unsafe content using Google Generative AI's safety features.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro") # Provider-identifying signal: "gemini-pro" model ID

    # When using generate_content, safety settings are applied automatically.
    # The response will include safety ratings.
    response = model.generate_content(text)

    # You can access safety ratings from the response
    # For a more explicit safety check without content generation,
    # one might use a dedicated moderation API if available,
    # but for LLM-based content, safety settings during generation are common.
    safety_feedback = response.prompt_feedback.safety_ratings if response.prompt_feedback else []

    # If the response also contains generated content, you might want to check its safety too
    # For this task, we're primarily concerned with the input prompt and potentially generated text safety.
    # The prompt_feedback applies to the input.
    # To check generated content, you would typically examine the response.candidates[0].safety_ratings

    return {
        "input_safety_ratings": [
            {"category": rating.category.name, "probability": rating.probability.name}
            for rating in safety_feedback
        ],
        # Add a placeholder for generated content safety if needed, or if the function were to generate content
        "generated_content_safety_ratings": [] # This would be populated if model.generate_content was actually generating
    }
