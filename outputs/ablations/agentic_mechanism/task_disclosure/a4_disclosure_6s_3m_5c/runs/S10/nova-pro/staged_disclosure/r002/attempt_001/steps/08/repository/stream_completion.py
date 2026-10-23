import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def stream_completion(prompt):
    response = bedrock.invoke_model(
        model_id='amazon.titan-text-express-v1',
        body={
            'inputText': prompt,
            'textGenerationConfig': {
                'maxTokenCount': 200,
                'stopSequences': [],
                'temperature': 0.5,
                'topP': 0.9
            }
        }
    )
    response_body = response['body'].read()
    response_json = json.loads(response_body)
    results = response_json.get('results', [])
    for result in results:
        yield result.get('outputText', '')

import json