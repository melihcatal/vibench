import boto3

def invoke_model():
    client = boto3.client('bedrock-runtime', region_name='us-west-2')
    model_id = 'anthropic.claude-v2'
    body = {'prompt': 'Hello, world!', 'max_tokens_to_sample': 100}
    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(body)
    )
    return response