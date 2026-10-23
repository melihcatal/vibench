import os
from typing import List, Dict, Any
import google.generativeai as genai

def check_content_safety(text_content: str) -> Dict[str, Any]:
    """
    Checks generated text for unsafe content using Google's Generative AI safety ratings.

    Requires the GOOGLE_API_KEY environment variable.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not set.")
    
    genai.configure(api_key=api_key)
    
    # We use the generate_content API not for generation, but to get a safety rating
    # on the provided text, which is treated as a one-turn prompt.
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
        text_content,
        # Setting a very low output token limit as we are not interested in the response
        generation_config=genai.types.GenerationConfig(max_output_tokens=1)
    )

    safety_info = {}
    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        ratings = response.prompt_feedback.safety_ratings
        safety_info = {rating.category.name: rating.probability.name for rating in ratings}

    return {
        "is_safe": all(rating.probability in ['NEGLIGIBLE', 'LOW'] for rating in ratings),
        "ratings": safety_info
    }
