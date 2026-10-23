from openai import OpenAI

from embeddings_client import load_config


def multilingual_query_translate(query: str, target_language: str = "en"):
    config = load_config()
    client = OpenAI(api_key=config.api_key, base_url=config.base_url)
    response = client.responses.create(model="gpt-4.1-mini", input=f"Translate this query to {target_language}: {query}")
    return {"provider": "openai", "translation": response.output_text}
