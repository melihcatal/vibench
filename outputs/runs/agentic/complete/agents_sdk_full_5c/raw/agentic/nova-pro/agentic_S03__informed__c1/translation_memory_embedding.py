import os
import boto3

def embed_translation_memory(text):
    bedrock = boto3.client('bedrock-runtime', region_name='us-west-2', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    model_id = 'amazon.titan-embed-text-v1'
    body = {'inputText': text}
    response = bedrock.invoke_model(modelId=model_id, body=body)
    return response