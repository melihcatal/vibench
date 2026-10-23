import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

api_key = os.getenv("IBM_NLU_APIKEY")
url = os.getenv("IBM_NLU_URL")
version = "2021-08-01"

authenticator = IAMAuthenticator(api_key)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version=version, authenticator=authenticator
)
natural_language_understanding.set_service_url(url)


def embed_text(text):
    response = natural_language_understanding.analyze(
        text=text, features=Features(sentiment=SentimentOptions())
    ).get_result()
    return response["sentiment"]["document"]["label"]
