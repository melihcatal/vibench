import os
import google.generativeai as genai

def check_annotation_safety(text: str) -> dict:
    """
    Checks free-text metric labels or annotations for unsafe text using Google Generative AI.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # Use a Generative AI model that supports safety attributes
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(text, safety_settings=[
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ])

    safety_ratings = {}
    if hasattr(response, 'prompt_feedback') and response.prompt_feedback.safety_ratings:
        for rating in response.prompt_feedback.safety_ratings:
            safety_ratings[rating.category.name] = rating.probability.name

    return {"text": text, "safety_ratings": safety_ratings}
