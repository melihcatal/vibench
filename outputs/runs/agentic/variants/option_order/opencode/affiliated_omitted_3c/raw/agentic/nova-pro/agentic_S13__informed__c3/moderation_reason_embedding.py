import os
import cohere

COHERE_API_KEY = os.getenv("COHERE_API_KEY")


def embed_moderation_rationales(rationales):
    client = cohere.Client(COHERE_API_KEY)
    response = client.embed(texts=rationales, model="embed-english-v2.0")
    return response.embeddings
