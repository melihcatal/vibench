import boto3

def invoke_model():
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(
        ModelId='amazon.titan-text-express-v1',
        Body={
            'inputText': 'Hello, world!'
        }
    )
    result = json.loads(response['Body'].read())
    return result['outputText']

if __name__ == '__main__':
    print(invoke_model())