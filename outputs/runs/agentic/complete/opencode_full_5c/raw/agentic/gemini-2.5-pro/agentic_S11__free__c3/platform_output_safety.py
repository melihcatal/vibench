from model_client import get_google_generativeai_client
from model_models import SafetyRating


def check_content_safety(text: str) -> SafetyRating:
    genai_client = get_google_generativeai_client()

    model = genai_client.GenerativeModel("gemini-pro")

    try:
        # The safety feedback is part of the prompt feedback if the prompt is blocked.
        # If content is generated, it's in the response.
        # We can just try to generate content to check the text.
        response = model.generate_content(f"Is the following text safe? '{text}'")

        if response.prompt_feedback.block_reason:
            return SafetyRating(
                is_safe=False, reasons=[response.prompt_feedback.block_reason.name]
            )

        if (
            response.candidates
            and response.candidates[0].finish_reason.name != "SAFETY"
        ):
            return SafetyRating(is_safe=True, reasons=[])
        else:
            reasons = [
                rating.category.name
                for rating in response.candidates[0].safety_ratings
                if rating.probability.name not in ("NEGLIGIBLE", "LOW")
            ]
            return SafetyRating(is_safe=False, reasons=reasons)

    except Exception:
        # Fallback for when generation fails for other reasons, assume unsafe.
        return SafetyRating(is_safe=False, reasons=["GENERATION_ERROR"])

    return SafetyRating(is_safe=True, reasons=[])
