import os
from azure.cognitiveservices.vision.contentmoderator.models import Screen
from document_client import get_azure_content_moderator_client

def moderate_vendor_text(text_content: str) -> Screen:
    client = get_azure_content_moderator_client()

    # Screen the text for profanity, classification, and personal data
    # The 'text_content' can be a vendor note, memo, or any free-form text field.
    # lang='eng' specifies the language of the text. Other languages are supported.
    # autocorrections=True can correct common typos before moderation.
    # pii=True to detect personally identifiable information.
    screen_result = client.text_moderation.screen_text(
        text_content=text_content,
        language='eng',
        autocorrect=True,
        pii=True
    )

    # The screen_result object contains various moderation details:
    #   .terms: detected profanity terms
    #   .classification: categories of unwanted content (sexual, suggestive, hate, self_harm, violence, etc.)
    #   .p_ii: personally identifiable information detection
    
    return screen_result
