import boto3
import json

def stream_completion(text):
    client = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-text-express-v1'
    body = {
        'inputText': text,
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
    result = json.loads(response['body'].read())
    for token in result['results'][0]['outputText'].split(' '):
        yield token