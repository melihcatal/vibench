import boto3


def summarize_embedding_job(job_id):
    client = boto3.client("bedrock-runtime")
    response = client.get_embedding_job(job_id=job_id)
    return response["summary"]
