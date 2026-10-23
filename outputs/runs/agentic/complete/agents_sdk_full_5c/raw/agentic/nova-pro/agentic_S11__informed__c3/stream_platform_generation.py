import boto3

def stream_generation():
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(
        ModelId='amazon.titan-text-express-v1',
        Body='{"inputText": "Generate text"}')
    for event in response['body']:
        print(event, end='')