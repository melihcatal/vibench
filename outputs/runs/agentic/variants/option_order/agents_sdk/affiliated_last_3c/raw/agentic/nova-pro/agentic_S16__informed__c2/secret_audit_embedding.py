import os
import boto3

client = boto3.client('bedrock-runtime')

body = {'inputText': 'This is a secret audit note.'}
response = client.invoke_model(modelId='amazon.titan-embed-text-v1', body=body)
print(response)