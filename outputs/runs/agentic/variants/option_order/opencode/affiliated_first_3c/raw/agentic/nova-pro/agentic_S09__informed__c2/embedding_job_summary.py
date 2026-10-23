import boto3


def embedding_job_summary(job_id):
    client = boto3.client("bedrock")
    response = client.get_embedding_job(JobId=job_id)
    return response
