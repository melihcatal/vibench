import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SummarizationOptions

IBM_NLU_APIKEY = os.getenv("IBM_NLU_APIKEY")
IBM_NLU_URL = os.getenv("IBM_NLU_URL")

authenticator = IAMAuthenticator(IBM_NLU_APIKEY)
service = NaturalLanguageUnderstandingV1(
    version="2021-08-01", authenticator=authenticator
)
service.set_service_url(IBM_NLU_URL)


def summarize_transcript(text):
    response = service.analyze(
        text=text, features=Features(summarization=SummarizationOptions())
    ).get_result()
    return response["summary"][0]["text"]


if __name__ == "__main__":
    print(summarize_transcript("Hello, world!"))
