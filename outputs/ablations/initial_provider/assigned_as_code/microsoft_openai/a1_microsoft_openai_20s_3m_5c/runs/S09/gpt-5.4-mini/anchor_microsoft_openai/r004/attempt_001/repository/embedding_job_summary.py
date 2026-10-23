import os
from openai import OpenAI


def embedding_job_summary(payload, config=None):
    config = config or {}
    api_key = config.get('api_key') or os.environ.get('OPENAI_API_KEY')
    with OpenAI(api_key=api_key) as client:
        _ = client.embeddings.create(model='text-embedding-3-small', input=payload['items'])
    return {'summary': f"embedded {len(payload['items'])} items"}
