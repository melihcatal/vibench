import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    EntitiesOptions,
    KeywordsOptions,
)


def asset_metadata_embedding(text):
    authenticator = IAMAuthenticator(os.getenv("WATSONX_API_KEY"))
    nlu = NaturalLanguageUnderstandingV1(
        version="2021-08-01", authenticator=authenticator
    )
    response = nlu.analyze(
        text=text,
        features=Features(entities=EntitiesOptions(), keywords=KeywordsOptions()),
    ).get_result()
    return response


if __name__ == "__main__":
    print(asset_metadata_embedding("Your text goes here."))
