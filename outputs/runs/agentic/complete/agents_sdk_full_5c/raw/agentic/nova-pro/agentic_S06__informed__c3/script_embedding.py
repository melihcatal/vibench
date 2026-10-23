import os
import boto3

def embed_script(text):
    bedrock = boto3.client('bedrock-runtime', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = bedrock.invoke_model(
        body=text,
        modelId='amazon.titan-embed-text-v1'
    )
    return response['embedding']