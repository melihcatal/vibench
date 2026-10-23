from cohere import Client

MODEL = "embed-english-v3.0"


def moderation_reason_embedding(texts):
    client = Client(api_key=None)
    result = client.embed(texts=texts, model=MODEL, input_type="search_document")
    return result.embeddings
