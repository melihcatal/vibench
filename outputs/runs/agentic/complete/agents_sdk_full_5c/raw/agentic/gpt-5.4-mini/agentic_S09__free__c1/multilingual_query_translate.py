from openai import OpenAI

from embeddings_client import get_openai_embeddings_client


OPENAI_TRANSLATION_MODEL = "gpt-4.1-mini"


def multilingual_query_translate(query: str, target_language: str = "en"):
    client: OpenAI = get_openai_embeddings_client()
    prompt = f"Translate the following search query into {target_language} and return only the translated text: {query}"
    response = client.responses.create(model=OPENAI_TRANSLATION_MODEL, input=prompt)
    return response.output_text
