import boto3

def invoke_model():
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(
        ModelId='amazon.titan-text-express-v1',
        Body='{"inputText": "Hello, world!"}'
    )
    result = json.loads(response['Body'].read())
    print(result)

if __name__ == '__main__':
    invoke_model()