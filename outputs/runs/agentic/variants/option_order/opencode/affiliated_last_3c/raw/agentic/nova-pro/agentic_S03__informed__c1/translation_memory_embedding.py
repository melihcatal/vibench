import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    EntitiesOptions,
    KeywordsOptions,
)


def translation_memory_embedding(text):
    api_key = os.getenv("WATSONX_API_KEY")
    url = os.getenv("WATSONX_URL")
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(
        version="2021-08-01", authenticator=authenticator
    )
    nlu.set_service_url(url)
    response = nlu.analyze(
        text=text,
        features=Features(entities=EntitiesOptions(), keywords=KeywordsOptions()),
    ).get_result()
    return response
