import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    EntitiesOptions,
    KeywordsOptions,
)

authenticator = IAMAuthenticator(os.getenv("IBM_STT_APIKEY"))
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version="2019-07-12", authenticator=authenticator
)
natural_language_understanding.set_service_url(os.getenv("IBM_STT_URL"))


def caption_embedding(text):
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(entities=EntitiesOptions(), keywords=KeywordsOptions()),
    ).get_result()
    return response
