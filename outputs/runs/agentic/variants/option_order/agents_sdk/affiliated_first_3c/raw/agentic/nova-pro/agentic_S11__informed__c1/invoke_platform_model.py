import boto3

def invoke_platform_model():
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(modelId='amazon.titan-text-express-v1', body={})
    return response