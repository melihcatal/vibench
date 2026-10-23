from azure.cognitiveservices.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials
import os

def moderate_profile_text(text: str) -> dict:
    """
    Moderates profile text using Azure Content Moderator before account activation.
    """
    # Retrieve Azure Content Moderator credentials from environment variables
    content_moderator_key = os.environ.get("AZURE_CONTENT_MODERATOR_KEY")
    content_moderator_endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")

    if not content_moderator_key or not content_moderator_endpoint:
        raise ValueError("AZURE_CONTENT_MODERATOR_KEY and/or AZURE_CONTENT_MODERATOR_ENDPOINT environment variables not set.")

    try:
        # Create a Content Moderator client
        client = ContentModeratorClient(
            endpoint=content_moderator_endpoint,
            credentials=CognitiveServicesCredentials(content_moderator_key)
        )

        # Perform text moderation
        # The `text.screen_text` method screens text for profanity, classifications, and personally identifiable information.
        # This is a simplified example; a real implementation would parse the full response.
        screen_result = client.text_moderation.screen_text(
            text_content=text,
            language='eng',
            autocorrect=True,
            pii=True,
            classify=True
        )

        # Extracting a simplified moderation status
        is_profane = False
        if screen_result.terms:
            is_profane = True

        # Classifications (e.g., adult, racy, offensive)
        classification_summary = None
        if screen_result.classification:
            classification_summary = {
                "category1": screen_result.classification.category1.score if screen_result.classification.category1 else 0,
                "category2": screen_result.classification.category2.score if screen_result.classification.category2 else 0,
                "category3": screen_result.classification.category3.score if screen_result.classification.category3 else 0,
                "review_recommended": screen_result.classification.review_recommended
            }

        return {
            "success": True,
            "is_profane": is_profane,
            "classification_summary": classification_summary,
            "raw_moderation_result": screen_result.as_dict() # Return full dict for detailed analysis
        }
    except Exception as e:
        return {"success": False, "message": str(e)}
