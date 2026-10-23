import os
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials

def check_annotation_safety(text_to_check: str) -> dict:
    key = os.environ.get('AZURE_CONTENT_MODERATOR_KEY')
    endpoint = os.environ.get('AZURE_CONTENT_MODERATOR_ENDPOINT')

    client = ContentModeratorClient(endpoint, CognitiveServicesCredentials(key))

    # Check for profanity
    screen_result = client.text_moderation.screen_text(text_content=text_to_check, language='eng', classify=False)

    # Check for personal identifiable information (PII) - requires separate classification, this is a simpler profanity/adult check
    # For full PII, a more advanced service or custom logic would be needed.

    is_unsafe = False
    details = {
        "profanity_detection": {
            "terms": [],
            "ismatched": screen_result.result == True if screen_result.result is not None else False
        }
    }

    if screen_result.terms:
        is_unsafe = True
        for term in screen_result.terms:
            details["profanity_detection"]["terms"].append({
                "index": term.index,
                "original_term": term.original_text,
                "suggested_term": term.list_id if term.list_id else ""
            })

    return {"is_safe": not is_unsafe, "details": details}