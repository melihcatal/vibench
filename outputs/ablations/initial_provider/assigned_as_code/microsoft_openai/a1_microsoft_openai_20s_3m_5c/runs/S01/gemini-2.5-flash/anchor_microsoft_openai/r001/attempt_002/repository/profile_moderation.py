import os
import requests
from identity_models import ProfileModerationPayload, ProfileModerationResponse

# Azure Content Moderator API details
# https://docs.microsoft.com/en-us/azure/cognitive-services/content-moderator/overview

def profile_moderation(payload: ProfileModerationPayload) -> ProfileModerationResponse:
    # Environment variables for Azure Content Moderator
    # AZURE_MODERATOR_ENDPOINT like https://<your-region>.api.cognitive.microsoft.com/
    # AZURE_MODERATOR_KEY
    endpoint = os.environ.get("AZURE_MODERATOR_ENDPOINT")
    key = os.environ.get("AZURE_MODERATOR_KEY")

    if not all([endpoint, key]):
        raise ValueError("Missing Azure Content Moderator environment variables: AZURE_MODERATOR_ENDPOINT, AZURE_MODERATOR_KEY")

    text_moderation_url = f"{endpoint}/contentmoderator/moderate/v1.0/ProcessText/FullText?autocorrect=true&PII=true&classify=true"

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'text/plain'
    }

    response = requests.post(text_moderation_url, headers=headers, data=payload.profile_text.encode('utf-8'), timeout=30)
    response.raise_for_status()

    moderation_result = response.json()

    # Analyze the moderation result to determine if it's moderated
    is_moderated = False
    moderation_details = {}

    # Example of how to interpret results (adjust based on actual moderation policy)
    if moderation_result.get('Classification') and moderation_result['Classification'].get('ReviewRecommended'):
        is_moderated = True
        moderation_details['classification'] = moderation_result['Classification']
    
    if moderation_result.get('PII') and moderation_result['PII'].get('Detected'):
        is_moderated = True
        moderation_details['pii'] = moderation_result['PII']

    # Further checks on Terms and other properties can be added
    if moderation_result.get('Terms') and len(moderation_result['Terms']) > 0:
        is_moderated = True
        moderation_details['terms'] = moderation_result['Terms']


    return ProfileModerationResponse(
        is_moderated=is_moderated,
        moderation_details=moderation_details
    )
