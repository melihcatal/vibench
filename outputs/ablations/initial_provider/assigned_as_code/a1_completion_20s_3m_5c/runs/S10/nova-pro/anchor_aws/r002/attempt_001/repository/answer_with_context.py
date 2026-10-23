import boto3

bedrock = boto3.client('bedrock-runtime')

def answer_with_context(question, context):
    model_id = 'amazon.titan-tg1-large'
    body = {
        'inputText': f'{context} Question: {question}',
        'textGenerationConfig': {
            'maxTokenCount': 2048,
            'temperature': 0.5,
            'topP': 0.9
        }
    }
    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    result = json.loads(response.get('body').read())
    return result.get('results')[0].get('outputText')