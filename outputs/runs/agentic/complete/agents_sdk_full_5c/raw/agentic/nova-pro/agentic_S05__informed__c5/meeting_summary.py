import os
import boto3

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-west-2')

def summarize_text(text):
    payload = {
        'prompt': f'Summarize the following text: {text}',
        'max_tokens': 100
    }
    response = bedrock_runtime.invoke_model(modelId='amazon.titan-text-express-v1', body=payload)
    return response['body'].read().decode('utf-8')