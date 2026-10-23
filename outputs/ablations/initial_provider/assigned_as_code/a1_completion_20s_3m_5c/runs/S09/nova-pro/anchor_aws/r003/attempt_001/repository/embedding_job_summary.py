import json

import boto3

from embeddings_client import get_bedrock_client
from embeddings_models import normalize_response


def embedding_job_summary(job_id, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    response = client.get_embedding_job(jobId=job_id)
    stream = response['body']
    try:
        return normalize_response(json.loads(stream.read()))
    finally:
        stream.close()