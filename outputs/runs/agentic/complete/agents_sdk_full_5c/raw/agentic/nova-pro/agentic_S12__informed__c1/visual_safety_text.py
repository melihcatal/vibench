import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

authenticator = IAMAuthenticator(os.getenv('IBM_API_KEY_ID'))
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-03-16',
    authenticator=authenticator
)

def check_safety(text):
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(sentiment=SentimentOptions())
    ).get_result()
    return response['sentiment']['document']['label']