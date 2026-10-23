import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv('IBM_API_KEY_ID'))
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
)

def summarize_job(text):
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(concepts=ConceptsOptions())).get_result()
    return response['concepts']