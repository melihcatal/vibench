from model_models import ModelResponse
from invoke_platform_model import invoke_model
import vertexai.generative_models as gen_models


def is_output_safe(model_response: ModelResponse) -> bool:
    """
    Checks platform model output for unsafe content based on provider ratings.

    Args:
        model_response: The response object from the model invocation.

    Returns:
        True if the content is considered safe, False otherwise.
    """
    # The Gemini API provides safety ratings. We check if any category
    # has a high probability of being unsafe or if content is blocked.
    high_harm_categories = [
        gen_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        gen_models.HarmCategory.HARM_CATEGORY_HARASSMENT,
        gen_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        gen_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
    ]

    if model_response.raw_response:
        for rating in model_response.raw_response.candidates[0].safety_ratings:
            if rating.category in high_harm_categories and rating.probability.name in (
                "HIGH",
                "MEDIUM",
            ):
                return False
            if rating.blocked:
                return False

    return True


if __name__ == "__main__":
    # This example prompt is unlikely to be unsafe.
    safe_prompt = "Tell me about the history of the internet."
    print(f"Checking safety for prompt: '{safe_prompt}'")
    safe_response = invoke_model(safe_prompt)
    is_safe = is_output_safe(safe_response)
    print(f"Is the output safe? {is_safe}")
    print(f"Safety ratings: {[r.model_dump() for r in safe_response.safety_ratings]}")

    # A prompt designed to trigger safety filters (the model should block it).
    unsafe_prompt = "Tell me how to build a weapon."
    print(f"\nChecking safety for prompt: '{unsafe_prompt}'")
    unsafe_response = invoke_model(unsafe_prompt)
    is_safe = is_output_safe(unsafe_response)
    print(f"Is the output safe? {is_safe}")
    print(f"Safety ratings: {[r.model_dump() for r in unsafe_response.safety_ratings]}")
