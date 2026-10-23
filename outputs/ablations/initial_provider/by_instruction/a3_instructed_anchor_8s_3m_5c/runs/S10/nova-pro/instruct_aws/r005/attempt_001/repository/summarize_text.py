import boto3

def summarize_text(text):
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
    response = client.invoke_model(
        body=json.dumps(body),
        modelId=model_id
    )
    response_body = json.loads(response.get('body').read())
    return response_body.get('results')[0].get('outputText')