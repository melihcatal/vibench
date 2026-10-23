import boto3

bedrock = boto3.client('bedrock-runtime')

def stream_completion(prompt):
    model_id = 'amazon.titan-text-express-v1'
    body = {
        'inputText': prompt,
        'textGenerationConfig': {
            'maxTokenCount': 500,
            'stopSequences': [],
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

    response_body = json.loads(response.get('body').read())
    output_text = response_body.get('results')[0].get('outputText')

    for token in output_text:
        yield token