import boto3

def get_bedrock_client(region_name='us-east-1'):
    return boto3.client('bedrock-runtime', region_name=region_name)

def invoke_model(client, model_id, body):
    return client.invoke_model(model_id=model_id, body=body)