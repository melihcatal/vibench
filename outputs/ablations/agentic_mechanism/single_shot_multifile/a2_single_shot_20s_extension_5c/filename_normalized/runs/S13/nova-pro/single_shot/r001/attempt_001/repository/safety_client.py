import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def get_safety_client():
    authenticator = IAMAuthenticator(os.getenv('IBM_WATSON_API_KEY'))
    service = NaturalLanguageUnderstandingV1(version='2021-08-01', authenticator=authenticator)
    service.set_service_url(os.getenv('IBM_WATSON_URL'))
    return service