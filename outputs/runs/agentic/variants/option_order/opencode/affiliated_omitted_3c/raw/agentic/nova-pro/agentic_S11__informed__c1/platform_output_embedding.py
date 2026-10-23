from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv("WATSONX_API_KEY"))
nlu = NaturalLanguageUnderstandingV1(version="2022-04-07", authenticator=authenticator)


def embed_text(text):
    response = nlu.analyze(
        text=text, features=Features(entities=EntitiesOptions())
    ).get_result()
    return response
