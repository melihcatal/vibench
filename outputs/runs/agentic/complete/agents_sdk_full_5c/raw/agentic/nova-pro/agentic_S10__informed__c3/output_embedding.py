import os
import boto3

client = boto3.client('bedrock-runtime', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def embed_text(text):
    response = client.invoke_model(
        modelId='amazon.titan-embed-text-v1',
        body={'inputText': text}
    )
    return response['embedding']