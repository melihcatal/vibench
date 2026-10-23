import os
import requests
from speech_models import ContentModerationPayload

# Azure Content Moderator API endpoint and key
# https://learn.microsoft.com/en-us/azure/ai-services/content-moderator/text-moderation-api

def check_script_safety(payload: ContentModerationPayload, config: dict = None):
    api_key = config.get('api_key') or os.environ.get("AZURE_CONTENT_MODERATOR_KEY")
    endpoint = config.get('endpoint') or os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")

    if not api_key or not endpoint:
        raise ValueError("Azure Content Moderator API key and endpoint must be provided or set as environment variables AZURE_CONTENT_MODERATOR_KEY and AZURE_CONTENT_MODERATOR_ENDPOINT.")

    text_moderation_url = f"{endpoint}contentmoderator/moderate/v3.0/ProcessText/Screen?classify=True"

    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Content-Type': 'text/plain',
    }

    try:
        response = requests.post(text_moderation_url, headers=headers, data=payload.text.encode('utf-8'))
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)
        moderation_result = response.json()

        # Process the moderation result as needed
        # For example, check for profanity, personal information, etc.
        is_safe = True
        violations = []

        if 'Classification' in moderation_result and moderation_result['Classification']['ReviewRecommended']:
            is_safe = False
            violations.append("Review Recommended by Classifier")
        
        if 'PII' in moderation_result and moderation_result['PII']['Detected']:
            is_safe = False
            violations.append("Personal Identifiable Information Detected")

        if 'Profanity' in moderation_result and moderation_result['Profanity']['Detected']:
            is_safe = False
            violations.append("Profanity Detected")
        
        # Add more checks as per Content Moderator capabilities

        return {"is_safe": is_safe, "violations": violations, "raw_result": moderation_result}

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error calling Azure Content Moderator API: {e}")
