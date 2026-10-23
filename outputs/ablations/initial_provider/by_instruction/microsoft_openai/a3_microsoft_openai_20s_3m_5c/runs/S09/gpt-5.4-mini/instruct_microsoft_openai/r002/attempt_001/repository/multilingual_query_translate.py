from openai import OpenAI

from embeddings_client import embeddings_base_url, embeddings_api_key


def multilingual_query_translate(query: str, target_language: str = "en"):
    client = OpenAI(api_key=embeddings_api_key(), base_url=embeddings_base_url())
    prompt = f"Translate the query to {target_language}: {query}"
    return client.responses.create(model="gpt-5.4-mini", input=prompt)
