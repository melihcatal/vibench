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


def embed_for_search(query, documents):
    query_response = natural_language_understanding.analyze(
        text=query, features=Features(sentiment=SentimentOptions())
    ).get_result()
    query_embedding = query_response["sentiment"]["document"]["label"]
    document_embeddings = []
    for doc in documents:
        doc_response = natural_language_understanding.analyze(
            text=doc, features=Features(sentiment=SentimentOptions())
        ).get_result()
        document_embeddings.append(doc_response["sentiment"]["document"]["label"])
    return query_embedding, document_embeddings
