import boto3
from bedrock_client import BedrockClient

def stream_output(model_id):
    client = BedrockClient()
    response = client.invoke_model(model_id=model_id, stream=True)
    for chunk in response:
        yield chunk

if __name__ == '__main__':
    model_id = 'amazon.titan-text-express-v1'
    for chunk in stream_output(model_id):
        print(chunk)