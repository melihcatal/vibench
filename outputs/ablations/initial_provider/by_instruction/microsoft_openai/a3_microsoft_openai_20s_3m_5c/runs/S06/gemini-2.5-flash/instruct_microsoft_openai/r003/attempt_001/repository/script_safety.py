import os
from azure.cognitiveservices.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials
from speech_models import SafetyCheckRequest

def check_script_safety(request: SafetyCheckRequest) -> dict:
    subscription_key = os.environ.get("AZURE_CONTENT_MODERATOR_KEY")
    endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")

    if not subscription_key or not endpoint:
        raise ValueError("AZURE_CONTENT_MODERATOR_KEY and AZURE_CONTENT_MODERATOR_ENDPOINT environment variables must be set.")

    client = ContentModeratorClient(
        endpoint=endpoint,
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    # Screen the text
    # See https://learn.microsoft.com/en-us/azure/ai-services/content-moderator/text-moderation-api for details
    text_screen = client.text_moderation.screen_text(
        text_content=request.text,
        language="eng", # Assuming English for now, could be dynamic
        autocorrect=True,
        pii=True,
        list_id=None
    )

    return text_screen.as_dict()
