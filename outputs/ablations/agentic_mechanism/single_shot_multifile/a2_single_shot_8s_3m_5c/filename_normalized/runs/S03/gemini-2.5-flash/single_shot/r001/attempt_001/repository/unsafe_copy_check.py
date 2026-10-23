import os
from azure.cognitiveservices.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials

def check_unsafe_content(text_content: str, language: str = "eng") -> dict:
    subscription_key = os.getenv("AZURE_CONTENT_MODERATOR_KEY")
    endpoint = os.getenv("AZURE_CONTENT_MODERATOR_ENDPOINT")

    if not subscription_key or not endpoint:
        raise ValueError("AZURE_CONTENT_MODERATOR_KEY and AZURE_CONTENT_MODERATOR_ENDPOINT environment variables must be set.")

    client = ContentModeratorClient(
        endpoint=endpoint,
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    # The screen_text method provides detailed content moderation.
    # It can detect profanity, classifications, PII, etc.
    # The language parameter helps with language-specific moderation rules.
    screen = client.text_moderation.screen_text(
        text_content=text_content,
        language=language,
        classify=True # Request classification details
    )

    # The response object 'screen' contains various moderation results.
    # For simplicity, we return a dictionary representation of the relevant parts.
    result = {
        "original_content": text_content,
        "profanity_found": len(screen.terms) > 0 if screen.terms else False,
        "profanity_terms": [t.term for t in screen.terms] if screen.terms else [],
        "classification": screen.classification.as_dict() if screen.classification else None,
        "review_recommended": screen.classification.review_recommended if screen.classification else False
    }
    return result
