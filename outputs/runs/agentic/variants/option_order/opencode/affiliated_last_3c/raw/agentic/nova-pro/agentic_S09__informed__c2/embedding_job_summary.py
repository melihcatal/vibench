import os
import boto3


def summarize_embedding_job(job_id):
    bedrock = boto3.client(
        "bedrock-runtime",
        region_name="us-west-2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    response = bedrock.get_embedding_job(jobId=job_id)
    return response["summary"]
