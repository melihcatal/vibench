import boto3

def stream_completion(text):
    client = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-text-express-v1'
    body = {
        'inputText': text,
        'textGenerationConfig': {
            'maxTokenCount': 4096,
            'temperature': 0,
            'topP': 0.9
        }
    }
    response = client.invoke_model_with_response_stream(
        body=json.dumps(body),
        modelId=model_id
    )
    for event in response.get('body'):
        chunk = event.get('chunk')
        if chunk:
            yield chunk.get('bytes').decode()