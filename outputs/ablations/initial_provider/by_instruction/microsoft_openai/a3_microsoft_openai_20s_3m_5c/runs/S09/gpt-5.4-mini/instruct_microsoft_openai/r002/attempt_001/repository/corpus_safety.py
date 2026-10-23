from openai import OpenAI

from embeddings_client import embeddings_base_url, embeddings_api_key


def corpus_safety(text: str):
    client = OpenAI(api_key=embeddings_api_key(), base_url=embeddings_base_url())
    return client.moderations.create(model="omni-moderation-latest", input=text)
