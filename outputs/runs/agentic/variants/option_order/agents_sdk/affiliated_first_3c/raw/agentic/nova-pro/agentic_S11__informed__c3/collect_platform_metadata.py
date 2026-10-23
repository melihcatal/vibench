import boto3

def collect_metadata():
    client = boto3.client('bedrock-runtime', region_name='us-west-2')
    response = client.invoke_model(
        modelId='amazon.titan-text-express-v1',
        body={
            'inputText': 'Hello, world!'
        }
    )
    return response