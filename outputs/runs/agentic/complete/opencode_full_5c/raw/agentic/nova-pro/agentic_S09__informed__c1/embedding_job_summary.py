import os
import boto3

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

bedrock = boto3.client(
    "bedrock-runtime",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name="us-west-2",
)


def summarize_embedding_job_results(job_id):
    response = bedrock.get_embedding_job(JobId=job_id)
    return response["Summary"]
