import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def embed_text(text):
    authenticator = IAMAuthenticator(os.getenv("WATSONX_API_KEY"))
    nlu = NaturalLanguageUnderstandingV1(
        version="2021-08-01", authenticator=authenticator
    )
    response = nlu.analyze(
        text=text,
        features=NaturalLanguageUnderstandingV1.Features(entities=True, keywords=True),
    ).get_result()
    return response
