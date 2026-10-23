import os
import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-west-2', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def summarize_embedding_job(job_id):
    response = bedrock.invoke_model(modelId='amazon.titan-text-express-v1', body={"inputText": f'Summarize embedding job {job_id}'})
    return response['body'].read().decode('utf-8')