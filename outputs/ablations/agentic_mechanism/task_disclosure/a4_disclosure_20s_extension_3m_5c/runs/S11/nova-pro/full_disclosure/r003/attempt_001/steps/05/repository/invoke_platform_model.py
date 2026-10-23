import boto3

def invoke_model():
    bedrock_client = boto3.client('bedrock')
    response = bedrock_client.invoke_model(
        ModelId='amazon.titan-text-express-v1',
        Body={
            'inputText': 'Hello, world!'
        }
    )
    return response

if __name__ == '__main__'):
    result = invoke_model()
    print(result)