from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    EntitiesOptions,
    KeywordsOptions,
)


def secret_audit_embedding(text):
    authenticator = IAMAuthenticator(os.environ["WATSONX_API_KEY"])
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version="2023-04-20", authenticator=authenticator
    )
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(entities=EntitiesOptions(), keywords=KeywordsOptions()),
    ).get_result()
    return response
