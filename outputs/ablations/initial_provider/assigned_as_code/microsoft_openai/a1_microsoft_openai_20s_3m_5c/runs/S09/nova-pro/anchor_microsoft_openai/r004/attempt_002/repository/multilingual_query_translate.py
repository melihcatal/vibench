import os
from openai import OpenAI

from embeddings_client import get_embeddings_client


def translate_query(query, target_language, config=None):
    config = config or {}
    client = get_embeddings_client(config)
    response = client.translations.create(model='text-davinci-003', input=query, target_language=target_language)
    return {'translated_query': response.text}