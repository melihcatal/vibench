# [LATER-STEP] profile_moderation.py
from identity_models import ProfileModerationRequest, ProfileModerationResponse


# Dummy moderation logic (replace with real ML/keyword check service)
def moderate_profile_text(text: str) -> str:
    # Example policy: block any text containing "spam"
    if "spam" in text.lower():
        return "<MODERATED>"
    return text


def moderate_user_profile(
    request: ProfileModerationRequest,
) -> ProfileModerationResponse:
    moderated = moderate_profile_text(request.profile_text)
    return ProfileModerationResponse(
        moderated_text=moderated,
        action="approve" if moderated != "<MODERATED>" else "reject",
    )
