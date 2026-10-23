import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def stream_completion(text):
    model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
    body = {
        'prompt': text,
        'max_tokens_to_sample': 300
    }
    response = bedrock.invoke_model_with_response_stream(
        body=json.dumps(body),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    for event in response.get('body'):
        chunk = event.get('chunk')
        if chunk:
            yield chunk.get('bytes').decode()