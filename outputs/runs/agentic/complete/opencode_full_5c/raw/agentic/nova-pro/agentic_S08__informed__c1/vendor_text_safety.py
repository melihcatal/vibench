import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    EntitiesOptions,
    KeywordsOptions,
)


def vendor_text_safety(vendor_notes):
    authenticator = IAMAuthenticator(os.getenv("WATSONX_API_KEY"))
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version="2023-04-01", authenticator=authenticator
    )
    response = natural_language_understanding.analyze(
        text=vendor_notes,
        features=Features(entities=EntitiesOptions(), keywords=KeywordsOptions()),
    ).get_result()
    return response["entities"]
