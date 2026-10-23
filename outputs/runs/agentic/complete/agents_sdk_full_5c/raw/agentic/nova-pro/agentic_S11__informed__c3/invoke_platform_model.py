import boto3

def invoke_model():
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(
        ModelId='amazon.titan-text-express-v1',
        Body='{