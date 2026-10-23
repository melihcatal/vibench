import os

import cohere


def translation_memory_embedding(text: str):
    client = cohere.Client(os.environ["COHERE_API_KEY"])
    return client.embed(texts=[text], model="embed-english-v3.0").embeddings[0]
