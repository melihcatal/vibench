import boto3
import json

def get_bedrock_client():
    return boto3.client('bedrock-runtime')

def invoke_model(client, model_id, body):
    response = client.invoke_model(
        body=json.dumps(body),
        modelId=model_id
    )
    return json.loads(response.get('body').read())