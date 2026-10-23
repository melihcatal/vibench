from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from azure.cognitiveservices.vision.contentmoderator.models import Screen
from msrest.authentication import CognitiveServicesCredentials
from security_models import ContentSafetyRequest, ContentSafetyResponse
import os

def secret_label_safety(payload: dict, config: dict = None) -> dict:
    config = config or {}

    # Azure Content Moderator credentials
    subscription_key = os.environ.get("CONTENT_MODERATOR_KEY") or config.get('content_moderator_key')
    endpoint = os.environ.get("CONTENT_MODERATOR_ENDPOINT") or config.get('content_moderator_endpoint')

    if not subscription_key or not endpoint:
        raise ValueError("Content Moderator subscription key and endpoint must be provided or set in environment variables.")

    client = ContentModeratorClient(
        endpoint=endpoint,
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    request_payload = ContentSafetyRequest(text=payload['text'])

    # Screen the text for profanity and other unsafe content
    screen_result: Screen = client.text_moderation.screen_text(text_content=request_payload.text, language='eng')

    is_safe = True
    moderation_result = {
        "profanity_score": screen_result.profanity_score,
        "terms": [],
        "classification": {}
    }

    if screen_result.terms:
        is_safe = False
        for term in screen_result.terms:
            moderation_result["terms"].append({"term": term.term, "index": term.index})

    if screen_result.classification:
        if screen_result.classification.review_recommended:
            is_safe = False
        moderation_result["classification"] = {
            "category1": screen_result.classification.category1.score if screen_result.classification.category1 else None,
            "category2": screen_result.classification.category2.score if screen_result.classification.category2 else None,
            "category3": screen_result.classification.category3.score if screen_result.classification.category3 else None,
            "review_recommended": screen_result.classification.review_recommended,
        }

    response = ContentSafetyResponse(is_safe=is_safe, moderation_result=moderation_result)
    return {"safety_check_result": response.__dict__}
