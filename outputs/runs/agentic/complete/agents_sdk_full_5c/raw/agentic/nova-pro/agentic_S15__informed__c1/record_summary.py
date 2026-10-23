import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv('WATSONX_API_KEY'))
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
)

def summarize_record(text):
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(summary=SummaryOptions())
    ).get_result()
    return response['summary']