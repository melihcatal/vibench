import os
import boto3

client = boto3.client('bedrock-runtime')

def summarize_incident(logs):
    prompt = f'Summarize the following logs for incident review: {logs}'
    response = client.invoke_model(model_id='anthropic.claude-v2', body={"prompt": prompt, "max_tokens_to_sample": 500})
    return response['outputText']