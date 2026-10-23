from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials
import os

def platform_output_safety(text_output, config=None):
    config = config or {}
    subscription_key = os.environ.get("AZURE_CONTENT_MODERATOR_KEY", config.get("key"))
    endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT", config.get("endpoint"))

    if not all([subscription_key, endpoint]):
        raise ValueError("Azure Content Moderator key and endpoint must be provided.")

    client = ContentModeratorClient(
        endpoint=endpoint, credentials=CognitiveServicesCredentials(subscription_key)
    )

    # Text moderation
    # The Text moderation APIs are synchronous
    screen = client.text_moderation.screen_text(
        text_content=text_output, 
        language='eng',
        autocorrect=True,
        pii=True,
        classify=True
    )

    is_unsafe = False
    safety_results = {}

    if screen.classification:
        if screen.classification.category1.score > 0.5 or \
           screen.classification.category2.score > 0.5 or \
           screen.classification.category3.score > 0.5:
            is_unsafe = True
        safety_results["classification"] = {
            "category1": screen.classification.category1.score if screen.classification.category1 else 0,
            "category2": screen.classification.category2.score if screen.classification.category2 else 0,
            "category3": screen.classification.category3.score if screen.classification.category3 else 0,
            "review_recommended": screen.classification.review_recommended
        }
    
    if screen.terms:
        is_unsafe = True # If any terms are found, consider it unsafe
        safety_results["terms"] = [{
            "term": term.term,
            "index": term.index,
            "original_index": term.original_index
        } for term in screen.terms]

    return {"is_unsafe": is_unsafe, "safety_details": safety_results}
