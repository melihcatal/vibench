import boto3


def embedding_job_summary(job_id):
    client = boto3.client("bedrock-runtime")
    response = client.get_embedding_job(job_id=job_id)
    return response
