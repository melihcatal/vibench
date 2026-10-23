from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials
from security_models import Secret
import os

def check_text_for_safety(text: str) -> dict:
    subscription_key = os.environ.get("AZURE_CONTENT_MODERATOR_KEY")
    endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")

    if not subscription_key or not endpoint:
        raise ValueError("AZURE_CONTENT_MODERATOR_KEY and AZURE_CONTENT_MODERATOR_ENDPOINT environment variables must be set.")

    client = ContentModeratorClient(
        endpoint=endpoint,
        credentials=CognitiveServicesCredentials(subscription_key)
    )

    # Check for profanity in the text
    # The SDK provides a text_moderation attribute on the client
    # and screen_text method for detailed analysis.
    # Using the default language ('eng') for now.
    # For more comprehensive checks, you might use other parameters like 'classify'.
    screen_result = client.text_moderation.screen_text(text=text, language='eng')

    # Check for profanity detections
    has_profanity = False
    if screen_result.terms:
        has_profanity = True

    # Content Moderator also offers classification, but for 'unsafe text' as generally understood,
    # profanity and custom term lists are usually the primary checks.
    # For simplicity, we're focusing on profanity here. Classification results are more nuanced.

    return {
        "text": text,
        "has_profanity": has_profanity,
        "profanity_terms": [term.term for term in screen_result.terms] if screen_result.terms else [],
        # You can add more details from screen_result if needed, e.g., auto correction, PIIDetection
    }

def check_secret_labels_for_safety(secret: Secret) -> dict:
    safety_checks = {"secret_name": secret.name}

    if secret.tags:
        for key, value in secret.tags.items():
            # Check both tag key and tag value for unsafe text
            key_check = check_text_for_safety(key)
            value_check = check_text_for_safety(value)
            safety_checks[f"tag_key_{key}_safety"] = key_check
            safety_checks[f"tag_value_{key}_safety"] = value_check
    
    # Assuming secret notes could be stored in a specific tag, e.g., 'notes'
    if secret.tags and 'notes' in secret.tags:
        notes_check = check_text_for_safety(secret.tags['notes'])
        safety_checks["secret_notes_safety"] = notes_check

    return safety_checks
