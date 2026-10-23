import google.generativeai as genai
from model_client import get_model_client
from model_models import SafetyCheckResponse, SafetyRating


def check_prompt_safety(prompt: str) -> SafetyCheckResponse:
    """
    Checks a prompt for unsafe content using the model's safety ratings.
    """
    model = get_model_client()
    response = model.generate_content(prompt)

    is_safe = True
    ratings = []

    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        for rating in response.prompt_feedback.safety_ratings:
            ratings.append(
                SafetyRating(
                    category=rating.category.name, probability=rating.probability.name
                )
            )
            if rating.probability.name not in ["NEGLIGIBLE", "LOW"]:
                is_safe = False

    # Also check for blocked prompts
    if response.prompt_feedback and response.prompt_feedback.block_reason:
        is_safe = False

    return SafetyCheckResponse(is_safe=is_safe, ratings=ratings)


def check_generated_text_safety(text: str) -> SafetyCheckResponse:
    """
    A simplified check for generated text safety. In a real scenario,
    this would be part of the generation response itself.
    This function simulates a check on already-generated text.
    """
    model = get_model_client()
    # We ask the model to classify the safety of the text.
    prompt = f"Rate the safety of the following text and explain why. Text: '{text}'"
    response = model.generate_content(prompt)  # This response itself has safety ratings

    is_safe = True
    ratings = []
    if response.candidates and response.candidates[0].safety_ratings:
        for rating in response.candidates[0].safety_ratings:
            ratings.append(
                SafetyRating(
                    category=rating.category.name, probability=rating.probability.name
                )
            )
            if rating.probability.name not in ["NEGLIGIBLE", "LOW"]:
                is_safe = False

    return SafetyCheckResponse(is_safe=is_safe, ratings=ratings)
