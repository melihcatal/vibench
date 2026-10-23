import json

from embeddings_client import get_bedrock_client


def embedding_job_summary(job_id, config=None):
    client = get_bedrock_client(config)
    response = client.get_job(jobId=job_id)
    return {"summary": json.loads(response["body"].read())}