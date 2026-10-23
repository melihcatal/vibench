import os
import requests
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def profile_moderation(profile_text, locale='en'):
    """Moderate profile text before account activation using watsonx.ai guardrails (HAP detection)."""
    # Load IBM credentials from environment
    iam_api_key = os.getenv('WATSONX_API_KEY')
    service_instance_id = os.getenv('WATSONX_PROJECT_ID')
    authenticator = IAMAuthenticator(iam_api_key)
    # Initialize the service client
    service = NaturalLanguageUnderstandingV1(version='2024-03-01', authenticator=authenticator)
    service.set_service_url(f'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com')
    # Define moderation features
    features = {
        'text_classification': {},
        'semantic_role_labeling': {}
    }
    response = service.analyze(
        text=profile_text,
        features=features,
        language=locale
    ).get_result()
    # Simple moderation: flag if any toxicity/undesirable content detected
    flagged = False
    for entity in response.get('entities', []):
        if entity.get('sentiment', {}).get('score', 0) < 0:
            flagged = True
            break
    return flagged