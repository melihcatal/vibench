from typing import Dict, Any
from document_client import get_google_generative_ai_client


def check_text_safety(text: str) -> Dict[str, Any]:
    """
    Checks text for unsafe content using Google's Gemini Pro API safety ratings.
    """
    model = get_google_generative_ai_client()

    # The response to a generate_content request includes prompt_feedback,
    # which contains safety ratings. We can send the text as a prompt
    # and examine the feedback without consuming the model's response.
    # A payload with 0 max output tokens is a common pattern for this.
    response = model.generate_content(text, generation_config={"max_output_tokens": 0})

    safety_ratings = {}
    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        for rating in response.prompt_feedback.safety_ratings:
            safety_ratings[rating.category.name] = rating.probability.name

    return safety_ratings
