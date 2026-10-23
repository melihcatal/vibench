import os
import boto3

def moderation_summary(text):
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(model_id='amazon.titan-text-express-v1', body=text)
    return response['outputText']