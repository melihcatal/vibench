import boto3

client = boto3.client('bedrock-runtime')

response = client.invoke_model(
    modelId='amazon.titan-text-express-v1',
    body={
        'inputText': 'Hello, world!'
    }
)

print(response['body'].read().decode())
