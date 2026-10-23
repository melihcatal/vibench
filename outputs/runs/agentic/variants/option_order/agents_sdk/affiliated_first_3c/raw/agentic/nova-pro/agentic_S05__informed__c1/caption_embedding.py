import os
import boto3

def embed_caption(text):
    bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
    response = bedrock.invoke_model(ModelId='amazon.titan-embed-text-v1', Body=text)
    return response['Body'].read().decode('utf-8')