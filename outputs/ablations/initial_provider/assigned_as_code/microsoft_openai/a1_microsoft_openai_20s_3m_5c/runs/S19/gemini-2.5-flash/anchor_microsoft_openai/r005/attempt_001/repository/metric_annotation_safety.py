import os
from azure.cognitiveservices.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials

def metric_annotation_safety(payload, config=None):
    config = config or {}
    client = ContentModeratorClient(
        endpoint=os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT"),
        credentials=CognitiveServicesCredentials(os.environ.get("AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY"))
    )

    text_to_check = payload['annotation_text']
    review_id = client.text_moderation.screen_text(text_content=text_to_check, language='eng')
    
    # The screen_text method returns a Screen object that contains information about profanity and PII
    # For simplicity, we'll just return the raw result, but in a real scenario, you'd parse this.
    return {'safety_scan_result': review_id.as_dict()}
