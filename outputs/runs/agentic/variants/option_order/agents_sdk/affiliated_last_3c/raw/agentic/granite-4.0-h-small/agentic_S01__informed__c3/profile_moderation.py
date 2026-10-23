import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

def moderate_profile_text(text: str) -> str:
    """Moderate profile text before account activation using Azure Content Safety.
    Returns the sanitized text or the original text if no violations are found.
    """
    endpoint = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT')
    key = os.getenv('AZURE_CONTENT_SAFETY_KEY')
    if not endpoint or not key:
        raise RuntimeError("Azure Content Safety credentials not configured")
    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    # Send a moderation request for the text
    result = client.analyze_text(content=text, category='profanity')
    # result contains a list of detections; if none, return original text
    if not result.detected_categories or not result.detected_categories[0].violations:
        return text
    # If violations exist, return a cleaned placeholder (could be more sophisticated)
    return "[Content removed due to profanity]"
