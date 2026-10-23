import os
import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')

def summarize_embedding_job(job_id):
    response = bedrock.invoke_model(
        model_id='amazon.titan-text-express-v1',
        body={'inputText': f'Summarize embedding job {job_id}'}
    )
    return response['outputText']