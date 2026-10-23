from azure.ai.contentmoderator import ContentModerationClient
from azure.ai.contentmoderator.models import TextContent
from azure.core.credentials import AzureKeyCredential
from typing import Dict, Any
import os

def check_payload_safety(text_payload: str) -> Dict[str, Any]:
    # Retrieve endpoint and key from environment variables
    endpoint = os.environ.get("CONTENT_MODERATOR_ENDPOINT")
    key = os.environ.get("CONTENT_MODERATOR_SUBSCRIPTION_KEY")

    if not endpoint or not key:
        raise ValueError("CONTENT_MODERATOR_ENDPOINT and CONTENT_MODERATOR_SUBSCRIPTION_KEY environment variables must be set.")

    client = ContentModerationClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # The SDK provides methods for text moderation
    # For a simple check, we can use the screen_text method.
    # This method can detect profanity, classifications, PII, etc.
    # The details of what to check for depend on the specific safety requirements.
    
    # We'll perform a basic text screening for profanity and classification.
    # The `language` parameter can be set, e.g., "eng" for English.
    # The `classify` parameter can be set to True to get classifications.
    screen_response = client.text_moderation.screen_text(
        text_content=TextContent(text_payload),
        language="eng", # Assuming English content for demonstration
        classify=True  # Request content classification
    )

    # Process the response to extract relevant safety information
    safety_report = {
        "original_text": text_payload,
        "profanity_detected": False,
        "classification_results": None,
        "terms_found": []
    }

    if screen_response.pii:
        safety_report["pii_detected"] = screen_response.pii.as_dict()

    if screen_response.profanity_result and screen_response.profanity_result.terms:
        safety_report["profanity_detected"] = True
        safety_report["terms_found"] = [term.term for term in screen_response.profanity_result.terms]

    if screen_response.classification_result:
        safety_report["classification_results"] = screen_response.classification_result.as_dict()

    return safety_report
