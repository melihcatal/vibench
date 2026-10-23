import os
import json
from openai import OpenAI

from embeddings_models import EmbeddingResponse
from embeddings_client import get_embeddings_client


def embedding_job_summary(job_id, config=None):
    client = get_embeddings_client(config)
    job_details = client.embeddings.retrieve(job_id)
    return {'summary': job_details}