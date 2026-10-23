import os

from amazon.bedrock import client


def summarize_embedding_job(job_id, config=None):
    config = config or {}
    with client.BedrockClient(api_key=config.get("api_key") or os.environ["AMAZON_BEDROCK_API_KEY"]) as client:
        response = client.models.get_job_status(job_id=job_id)
    return response