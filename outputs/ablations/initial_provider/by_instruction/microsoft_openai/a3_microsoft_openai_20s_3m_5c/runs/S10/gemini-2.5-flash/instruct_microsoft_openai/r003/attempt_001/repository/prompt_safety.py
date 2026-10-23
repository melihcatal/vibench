import os
from azure.cognitiveservices.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials

def check_safety(text: str) -> dict:
    """
    Checks prompts and generated text for unsafe content using Azure Content Moderator.
    """
    # Ensure AZURE_CONTENT_MODERATOR_ENDPOINT and AZURE_CONTENT_MODERATOR_KEY environment variables are set
    MODERATOR_ENDPOINT = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")
    MODERATOR_KEY = os.environ.get("AZURE_CONTENT_MODERATOR_KEY")

    client = ContentModeratorClient(
        endpoint=MODERATOR_ENDPOINT,
        credentials=CognitiveServicesCredentials(MODERATOR_KEY)
    )

    # Text moderation
    text_screen = client.text_moderation.screen_text(
        text_content=text,
        language="eng",
        autocorrect=True,
        pii=True,
        list_id=None
    )

    return text_screen.as_dict()
