import os
from ibm_watsonx_ai.hap import HazardousAndPersonalContentDetection
from ibm_watsonx_ai.auth import MetadataExchangeTokenProvider
from ibm_cloud_sdk_core import get_authenticator_from_environment

WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
PROJECT_ID = os.getenv('WATSONX_PROJECT_ID')

token_provider = MetadataExchangeTokenProvider(apikey=WATSONX_API_KEY)
authenticator = get_authenticator_from_environment('watsonx')
authenticator.set_service_url('https://iam.cloud.ibm.com/identity/token')

hap_detector = HazardousAndPersonalContentDetection(authenticator=authenticator,
                                                    project_id=PROJECT_ID,
                                                    url='https://api.ibm.com/watsonx/v1/hap')

def moderate_profile_text(user_id: str, profile_text: str, locale: str = 'en') -> dict:
    content = {
        'user_id': user_id,
        'locale': locale,
        'text': profile_text
    }
    response = hap_detector.detect_content(body=[content])
    # The HAP API returns a list with a single safety rating
    rating = response[0]['safety']
    # Simple moderation rule: block if profanity or hate bias above threshold
    if rating['profanity'] > 0.5 or rating['hate_bias'] > 0.5:
        raise ValueError('Profile text contains unacceptable content')
    return {'rating': rating, 'moderation_passed': True}
