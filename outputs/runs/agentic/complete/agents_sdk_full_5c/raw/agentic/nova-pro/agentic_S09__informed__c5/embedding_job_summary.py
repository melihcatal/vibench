import os
import boto3

def summarize_embedding_job(job_id):
    bedrock = boto3.client('bedrock-runtime', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = bedrock.get_foundation_model(ModelId='amazon.titan-embed-text-v1')
    return response

if __name__ == '__main__':
    print(summarize_embedding_job('sample-job-id'))