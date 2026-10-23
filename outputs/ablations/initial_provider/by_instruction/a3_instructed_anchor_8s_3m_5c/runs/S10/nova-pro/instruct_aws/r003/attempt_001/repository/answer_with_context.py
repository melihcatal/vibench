import boto3

def answer_with_context(question, context):
    client = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-text-express-v1'
    body = {
        'inputText': f'{context} {question}',
        'textGenerationConfig': {
            'maxTokenCount': 512,
            'temperature': 0.5,
            'topP': 0.9
        }
    }
    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(body)
    )
    response_body = json.loads(response.get('body').read())
    return response_body.get('results')[0].get('outputText')