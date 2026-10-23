import boto3

def stream_generation():
    client = boto3.client('bedrock-runtime', region_name='us-west-2')
    body = {
        'prompt': 'Translate the following English text to French: Hello, how are you?',
        'max_tokens': 150,
        'temperature': 0.5,
        'top_p': 0.9
    }
    response = client.invoke_model(
        modelId='amazon.titan-text-express-v1',
        body=json.dumps(body)
    )
    for event in response['body'].events():
        yield event['chunk']