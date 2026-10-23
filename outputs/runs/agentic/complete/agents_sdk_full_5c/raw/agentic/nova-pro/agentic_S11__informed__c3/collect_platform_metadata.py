import boto3

def collect_metadata():
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(
        ModelId='amazon.titan-text-express-v1',
        Body='{"inputText": "Collect metadata"}')
    return response