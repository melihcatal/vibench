import os
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials

def moderate_text_claims(text_to_moderate: str) -> dict:
    """
    Moderates free-text claims or notes using Azure Content Moderator.
    """
    subscription_key = os.environ.get("AZURE_CONTENT_MODERATOR_KEY")
    endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")

    if not all([subscription_key, endpoint]):
        raise ValueError("Missing Azure Content Moderator environment variables.")

    client = ContentModeratorClient(
        endpoint=endpoint,
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    # Text moderation
    # For a full implementation, you would check for profanity, classification, etc.
    try:
        text_screen = client.text_moderation.screen_text(
            text_content=text_to_moderate,
            language="eng",
            autocorrect=True,
            pii=True,
        )
        return text_screen.as_dict()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage
    os.environ["AZURE_CONTENT_MODERATOR_KEY"] = "YOUR_AZURE_CONTENT_MODERATOR_KEY"
    os.environ["AZURE_CONTENT_MODERATOR_ENDPOINT"] = "https://your-region.api.cognitive.microsoft.com/contentmoderator"

    claim_text = "This is a test claim with some potentially offensive words like shit and damn."
    moderation_result = moderate_text_claims(claim_text)
    print(moderation_result)

    claim_text_clean = "This is a clean claim."
    moderation_result_clean = moderate_text_claims(claim_text_clean)
    print(moderation_result_clean)
