import os
from azure.ai.contentmoderator import ContentModeratorClient
from azure.core.credentials import AzureKeyCredential

def check_payload_safety(text_payload: str, endpoint: str, key: str) -> dict:
    # Create a Content Moderator client
    client = ContentModeratorClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # Moderate the text payload
    text_moderation_result = client.text.moderate_text(text_payload)

    # Extract relevant information
    safety_report = {
        "original_text": text_payload,
        "profanity_detection": {
            "terms": []
        },
        "classification_detection": {
            "category1": None,
            "category2": None,
            "category3": None,
            "review_recommended": False
        }
    }

    if text_moderation_result.profanity_terms:
        for term in text_moderation_result.profanity_terms:
            safety_report["profanity_detection"]["terms"].append({
                "term": term.term,
                "index": term.index
            })

    if text_moderation_result.classification:
        classification = text_moderation_result.classification
        safety_report["classification_detection"]["category1"] = classification.category1.score if classification.category1 else None
        safety_report["classification_detection"]["category2"] = classification.category2.score if classification.category2 else None
        safety_report["classification_detection"]["category3"] = classification.category3.score if classification.category3 else None
        safety_report["classification_detection"]["review_recommended"] = classification.review_recommended

    return safety_report

# Example usage (requires AZURE_CONTENT_MODERATOR_ENDPOINT and AZURE_CONTENT_MODERATOR_KEY env vars)
# endpoint = os.environ["AZURE_CONTENT_MODERATOR_ENDPOINT"]
# key = os.environ["AZURE_CONTENT_MODERATOR_KEY"]
# payload = "This is a test string with some profanity like damn and hell."
# safety_check_result = check_payload_safety(payload, endpoint, key)
# print(safety_check_result)
