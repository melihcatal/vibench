import os
from openai import OpenAI

from embeddings_client import get_embeddings_client


def summarize_embedding_job_results(job_id, config=None):
    config = config or {}
    client = get_embeddings_client(config)
    response = client.embeddings.retrieve(job_id)
    return {'summary': response.summary}