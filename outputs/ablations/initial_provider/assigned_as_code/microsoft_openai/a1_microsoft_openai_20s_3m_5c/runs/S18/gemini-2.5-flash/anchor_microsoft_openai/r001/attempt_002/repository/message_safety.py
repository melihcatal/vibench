import os
from azure.cognitiveservices.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials

def check_message_safety(text_content: str):
    subscription_key = os.environ.get("AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY")
    endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")

    if not subscription_key or not endpoint:
        raise ValueError("AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY or AZURE_CONTENT_MODERATOR_ENDPOINT environment variables not set.")

    client = ContentModeratorClient(
        endpoint=endpoint,
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    # Screen the text for profanity, sentiments
    screen = client.text_moderation.screen_text(
        text_content=text_content,
        language="eng",
        autocorrect=True,
        pii=True,
        list_id=None
    )

    is_safe = True
    if screen.terms:
        is_safe = False
    if screen.profanity_score and screen.profanity_score > 0.5:
        is_safe = False

    return {"is_safe": is_safe, "moderation_results": screen.as_dict()}
