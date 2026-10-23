import boto3

client = boto3.client('bedrock-runtime')

response = client.invoke_model(
    modelId='amazon.titan-text-express-v1',
    body={
        'inputText': 'Hello, world!'
    }
)

stream = response['body']

while True:
    chunk = stream.read(1024)
    if not chunk:
        break
    print(chunk.decode())
