import boto3
import json

bedrock = boto3.client('bedrock-runtime')

def stream_completion(text):
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
        contentType='application/json',
        stream=True
    )
    for event in response.get('body'):
        chunk = json.loads(event)
        yield chunk.get('results')[0].get('outputText')