import boto3
import json

EMBED_MODEL_ID = 'amazon.titan-embed-text-v1'

def embed_platform_output(text: str) -> list[float]:
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    body = json.dumps({'inputText': text})
    response = client.invoke_model(
        modelId=EMBED_MODEL_ID,
        body=body,
        contentType='application/json',
        accept='application/json'
    )
    response_body = json.loads(response['body'].read())
    return response_body['embedding']
