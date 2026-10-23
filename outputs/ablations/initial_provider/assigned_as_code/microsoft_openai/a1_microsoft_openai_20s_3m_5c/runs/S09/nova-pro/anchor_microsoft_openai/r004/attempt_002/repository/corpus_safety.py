import os
from openai import OpenAI

from embeddings_client import get_embeddings_client


def check_corpus_text(text, config=None):
    config = config or {}
    client = get_embeddings_client(config)
    response = client.moderations.create(input=text)
    return {'is_safe': response.results[0].flagged}