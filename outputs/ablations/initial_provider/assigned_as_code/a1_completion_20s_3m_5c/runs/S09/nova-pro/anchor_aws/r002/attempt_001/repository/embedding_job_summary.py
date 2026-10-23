import json

import boto3

from.embeddings_client import get_bedrock_client
from.embeddings_models import normalize_payload, parse_response


def embedding_job_summary(job_id, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    response = client.get_embedding_job(jobId=job_id)
    job_summary = parse_response(response["body"].read())
    return {"job_summary": job_summary}