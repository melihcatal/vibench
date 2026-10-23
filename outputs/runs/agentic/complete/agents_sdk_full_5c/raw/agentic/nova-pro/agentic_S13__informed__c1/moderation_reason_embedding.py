import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions

authenticator = IAMAuthenticator(os.getenv('WATSONX_API_KEY'))
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator
)
natural_language_understanding.set_service_url(os.getenv('WATSONX_URL'))

def moderation_reason_embedding(text):
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(entities=EntitiesOptions())).get_result()
    return response['entities']