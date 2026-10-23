import os
from openai import OpenAI

from embeddings_models import EmbeddingRequest, EmbeddingResponse
from embeddings_client import get_embeddings_client


def multilingual_query_translate(query, target_language, config=None):
    client = get_embeddings_client(config)
    translation_response = client.translations.create(model='text-davinci-003', source='auto', target=target_language, text=query)
    translated_query = translation_response.choices[0].text.strip()
    return {'translated_query': translated_query}