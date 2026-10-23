import boto3

bedrock = boto3.client('bedrock-runtime')

model_id = 'amazon.titan-text-express-v1'

def generate_stream(prompt):
    body = {
        'inputText': prompt,
        'textGenerationConfig': {
            'maxTokenCount': 4096,
            'temperature': 0,
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

    for event in response_body.get('results'):
        yield event
