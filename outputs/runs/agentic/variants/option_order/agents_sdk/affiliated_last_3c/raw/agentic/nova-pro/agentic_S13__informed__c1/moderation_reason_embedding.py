import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions

WATSONX_API_KEY = os.getenv('WATSONX_API_KEY')
WATSONX_URL = os.getenv('WATSONX_URL')

authenticator = IAMAuthenticator(WATSONX_API_KEY)
natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01', authenticator=authenticator)
natural_language_understanding.set_service_url(WATSONX_URL)

def moderation_reason_embedding(text):
    response = natural_language_understanding.analyze(
        text=text, features=Features(entities=EntitiesOptions())).get_result()
    return response
