import os
import boto3

client = boto3.client('bedrock-runtime', region_name='us-east-1')

response = client.invoke_model(
    model_id='anthropic.claude-v2',
    body={'prompt': 'Summarize the following error logs:', 'max_tokens_to_sample': 100}
)

print(response['body']['completions'][0]['text'])