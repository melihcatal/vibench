import os
import boto3

def stored_asset_summary(text):
    anthropic = boto3.client('bedrock-runtime', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = anthropic.invoke_model(modelId='anthropic.claude-v2', body={"prompt": f"Summarize this text: {text}", "max_tokens_to_sample": 300})
    return response['body'].read().decode('utf-8')