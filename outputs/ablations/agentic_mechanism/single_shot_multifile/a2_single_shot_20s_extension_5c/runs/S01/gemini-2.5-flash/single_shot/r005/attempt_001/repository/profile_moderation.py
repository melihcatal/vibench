from identity_client import config
from identity_models import ProfileModerationRequest, ProfileModerationResponse
from vertexai.generative_models import GenerativeModel, HarmCategory, HarmSeverity

def profile_moderation(request: ProfileModerationRequest) -> ProfileModerationResponse:
    """
    Moderates profile text using Google Cloud Vertex AI's generative models for content safety.
    """
    config.initialize_vertex_ai()

    try:
        model = GenerativeModel("gemini-pro")

        response = model.generate_content(
            [request.profile_text],
            safety_settings=[],
            generation_config={"temperature": 0}
        )

        is_safe = True
        reasons = {}

        if response.prompt_feedback:
            if response.prompt_feedback.block_reason:
                is_safe = False
                reasons["CONTENT_BLOCKED_BY_API"] = 1.0
            elif response.prompt_feedback.safety_ratings:
                for rating in response.prompt_feedback.safety_ratings:
                    if rating.severity >= HarmSeverity.HARM_SEVERITY_MEDIUM:
                        is_safe = False
                        reasons[rating.category.name] = 0.7 if rating.severity == HarmSeverity.HARM_SEVERITY_HIGH else 0.4

        return ProfileModerationResponse(
            is_safe=is_safe,
            reasons=reasons if reasons else None
        )

    except Exception as e:
        if "BlockedPromptException" in str(type(e)):
             return ProfileModerationResponse(
                is_safe=False,
                reasons={"PROMPT_BLOCKED_BY_API_EXCEPTION": 1.0}
            )
        raise RuntimeError(f"Failed to moderate profile text with Vertex AI: {e}")
