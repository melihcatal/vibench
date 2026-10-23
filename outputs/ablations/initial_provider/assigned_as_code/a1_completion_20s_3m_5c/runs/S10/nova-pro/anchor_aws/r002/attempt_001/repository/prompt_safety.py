import boto3

bedrock = boto3.client('bedrock-runtime')

def check_safety(text):
    model_id = 'amazon.titan-tg1-large'
    body = {
        'inputText': text,
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
    return 'safe' if 'safe' in result.get('results')[0].get('outputText') else 'unsafe'