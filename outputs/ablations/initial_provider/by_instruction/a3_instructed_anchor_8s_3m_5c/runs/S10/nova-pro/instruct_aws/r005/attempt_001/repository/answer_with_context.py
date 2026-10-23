import boto3

def answer_with_context(question, context):
    client = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-text-express-v1'
    body = {
        'inputText': f'{context} {question}',
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