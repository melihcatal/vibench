import os
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials
from typing import Dict, Any

def check_unsafe_content(text_content: str) -> Dict[str, Any]:
    """
    Checks localized copy for unsafe content using Azure Content Moderator.
    """
    # Replace with your Azure Content Moderator subscription key and endpoint
    SUBSCRIPTION_KEY = os.environ.get("AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY")
    ENDPOINT = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")

    client = ContentModeratorClient(
        endpoint=ENDPOINT,
        credentials=CognitiveServicesCredentials(SUBSCRIPTION_KEY)
    )

    # Screen the text for profanity, classifications, and personal data
    # Note: The text_content should ideally be in bytes or a stream for full API capabilities,
    # but for simplicity, we'll pass it directly as a string to the text_moderation operations.
    # For more advanced scenarios, consider encoding to bytes.
    screen_result = client.text_moderation.screen_text(
        text_content=text_content,
        language="eng", # Assuming English for moderation for simplicity, could be dynamic
        autocorrect=True,
        pii=True,
        classify=True
    )

    # Extract relevant information from the screening result
    # This part can be customized based on what specific details are needed.
    moderation_summary = {
        "original_text": text_content,
        "profanity_detection": {
            "terms": [{'term': t.term, 'index': t.index} for t in screen_result.terms] if screen_result.terms else [],
            "status": screen_result.status.description if screen_result.status else "N/A"
        },
        "classification": {
            "category1": screen_result.classification.category1.score if screen_result.classification and screen_result.classification.category1 else None,
            "category2": screen_result.classification.category2.score if screen_result.classification and screen_result.classification.category2 else None,
            "category3": screen_result.classification.category3.score if screen_result.classification and screen_result.classification.category3 else None,
            "review_recommended": screen_result.classification.review_recommended if screen_result.classification else False
        },
        "pii_detection": {
            "email": [e.text for e in screen_result.p_ii.email] if screen_result.p_ii and screen_result.p_ii.email else [],
            "phone": [p.text for p in screen_result.p_ii.phone] if screen_result.p_ii and screen_result.p_ii.phone else [],
            "address": [a.text for a in screen_result.p_ii.address] if screen_result.p_ii and screen_result.p_ii.address else []
        }
    }
    return moderation_summary
