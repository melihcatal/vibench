import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SummarizationOptions

authenticator = IAMAuthenticator(os.getenv('IBM_WATSON_API_KEY'))
service = NaturalLanguageUnderstandingV1(version='2021-08-01', authenticator=authenticator)
service.set_service_url(os.getenv('IBM_WATSON_URL'))

def moderation_summary(text):
    response = service.analyze(
        text=text,
        features=Features(summarization=SummarizationOptions())
    ).get_result()
    return response['summarization'][0]['text']