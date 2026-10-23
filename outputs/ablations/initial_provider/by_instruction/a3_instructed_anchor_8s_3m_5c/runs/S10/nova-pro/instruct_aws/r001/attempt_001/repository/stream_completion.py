import boto3
import json

def stream_completion(text):
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    model_id = 'amazon.titan-text-express-v1'
    response = client.invoke_model(
        model_id=model_id,
        body={
            'inputText': text,
            'textGenerationConfig': {
                'maxTokenCount': 200,
                'stopSequences': [],
                'temperature': 0.5,
                'topP': 0.9
            }
        }
    )
    result = json.loads(response['body'].read())
    for token in result['results'][0]['outputText']:
        yield token