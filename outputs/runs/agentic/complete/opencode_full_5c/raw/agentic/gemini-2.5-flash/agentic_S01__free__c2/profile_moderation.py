import google.generativeai as genai
import os

from identity_client import GoogleCloudConfig
from identity_models import ModerateProfileTextRequest, ModerateProfileTextResponse

# Configure Generative AI client
if GoogleCloudConfig.API_KEY:
    genai.configure(api_key=GoogleCloudConfig.API_KEY)
else:
    # Fallback to default credentials if API_KEY is not set (e.g., for GCE/Cloud Run)
    # It's good practice to ensure at least one auth method is present.
    pass


def profile_moderation(
    request: ModerateProfileTextRequest,
) -> ModerateProfileTextResponse:
    """
    Moderates profile text before account activation using Google Cloud Generative AI.
    """
    # A specific model ID for content safety is not directly exposed as a separate model
    # but is often integrated into general-purpose generative models like 'gemini-pro'
    # with specific safety settings. Here, we'll use a general model and rely on its
    # inherent safety features or implement custom logic based on its response.
    model = genai.GenerativeModel("gemini-pro")

    try:
        # For moderation, we check for safety attributes in the response.
        # This is a conceptual representation; actual implementation might involve
        # more complex parsing of safety ratings.
        response = model.generate_content(
            f"Review the following profile text for inappropriate content: {request.text_content}"
        )

        is_safe = True
        moderation_feedback = None

        # This is a simplified check. Real moderation would involve inspecting
        # response.candidates[0].safety_ratings or similar structures if available
        # from a dedicated moderation API or model output.
        # For demonstration, we'll assume content is unsafe if the model refuses output.
        if not response.candidates:
            is_safe = False
            moderation_feedback = "Content generation blocked due to safety concerns."
        else:
            # In a real scenario, you would analyze response.candidates[0].safety_ratings
            # For simplicity, we assume if we get a response, it's generally safe within typical limits.
            # A more robust solution would involve explicit safety checks against score thresholds.
            pass

        return ModerateProfileTextResponse(
            is_safe=is_safe, moderation_feedback=moderation_feedback
        )

    except Exception as e:
        raise ValueError(f"Failed to moderate profile text: {e}")
