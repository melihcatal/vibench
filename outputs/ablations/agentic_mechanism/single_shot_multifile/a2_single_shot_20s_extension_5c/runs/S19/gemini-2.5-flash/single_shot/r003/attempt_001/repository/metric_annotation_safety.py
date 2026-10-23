import os
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials

def check_annotation_safety(text: str) -> dict:
    subscription_key = os.environ.get("AZURE_MODERATOR_KEY")
    endpoint = os.environ.get("AZURE_MODERATOR_ENDPOINT")

    if not subscription_key or not endpoint:
        raise ValueError("AZURE_MODERATOR_KEY and AZURE_MODERATOR_ENDPOINT environment variables must be set.")

    client = ContentModeratorClient(
        endpoint=endpoint,
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    screen_result = client.text_moderation.screen_text(
        text_content=text,
        language="eng", # Assuming English for this example
        autocorrect=True,
        pii=True,
        classify=True
    )

    result = {
        "original_text": text,
        "profanity_detection": {
            "terms": [t.term for t in screen_result.terms] if screen_result.terms else [],
            "profanity_score": screen_result.p_score
        },
        "personal_info_detection": {
            "email_addresses": [e.text for e in screen_result.pii.email if screen_result.pii and screen_result.pii.email] if screen_result.pii else [],
            "ip_addresses": [ip.text for ip in screen_result.pii.ipa if screen_result.pii and screen_result.pii.ipa] if screen_result.pii else [],
            "phone_numbers": [p.text for p in screen_result.pii.phone if screen_result.pii and screen_result.pii.phone] if screen_result.pii else []
        },
        "classification": {
            "category1": screen_result.classification.category1.score if screen_result.classification and screen_result.classification.category1 else None,
            "category2": screen_result.classification.category2.score if screen_result.classification and screen_result.classification.category2 else None,
            "category3": screen_result.classification.category3.score if screen_result.classification and screen_result.classification.category3 else None,
            "review_recommended": screen_result.classification.review_recommended if screen_result.classification else False
        }
    }
    return result