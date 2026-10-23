import boto3
import json

def get_bedrock_client():
    return boto3.client('bedrock-runtime')

def invoke_model(client, model_id, body):
    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(body)
    )
    return json.loads(response['body'].read())