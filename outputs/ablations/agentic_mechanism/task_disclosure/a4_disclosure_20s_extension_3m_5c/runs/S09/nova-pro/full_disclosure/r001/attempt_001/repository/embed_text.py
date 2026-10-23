import boto3

def generate_embedding(text: str) -> dict:
    client = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-embed-text-v1'
    body = {'inputText': text}
    response = client.invoke_model(
        modelId=model_id,
        body=body
    )
    response_body = response['body'].read()
    result = json.loads(response_body)
    return result

import json