import os

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions


def moderation_reason_embedding(text):
    authenticator = IAMAuthenticator(os.getenv("WATSONX_API_KEY"))
    service = NaturalLanguageUnderstandingV1(
        version="2021-08-01", authenticator=authenticator
    )
    response = service.analyze(
        text=text, features=Features(entities=EntitiesOptions())
    ).get_result()
    return response
