import os
import boto3

client = boto3.client('bedrock-runtime', region_name='us-west-2', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def summarize_embedding_job(job_id):
    response = client.get_embedding_job(jobId=job_id)
    return response