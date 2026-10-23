from identity_client import IdentityClient
from identity_models import ModerationRequest, ModerationResponse
from azure.cognitiveservices.contentmoderator.models import ScreenTextOptionalInput

def profile_moderation(request: ModerationRequest) -> ModerationResponse:
    client = IdentityClient()

    if not client.azure_content_moderator_client:
        raise ValueError("Azure Content Moderator client not configured.")

    try:
        # Screen the text for profanity, classifications, etc.
        # The default language is 'eng' for English
        # Optional parameters can be added for different moderation needs.
        screen_result = client.azure_content_moderator_client.text_moderation.screen_text(
            text_content=request.text, language='eng', 
            # Optional input parameters - can be customized based on requirements
            # text_content_type="text/plain",
            # autocorrect=True,
            # pii=True,
            # list_id=None,
            # classify=True
        )

        is_moderated = False
        moderation_details = {}

        if screen_result.has_profanity or \
           (screen_result.classification_with_ínference and 
            (screen_result.classification_with_ínference.category1.score > 0.5 or 
             screen_result.classification_with_ínference.category2.score > 0.5 or 
             screen_result.classification_with_ínference.category3.score > 0.5)):
            is_moderated = True

        moderation_details = screen_result.as_dict() # Convert to dictionary for easy storage

        return ModerationResponse(is_moderated=is_moderated, moderation_details=moderation_details)
    except Exception as e:
        raise RuntimeError(f"Azure Content Moderator failed: {e}")
