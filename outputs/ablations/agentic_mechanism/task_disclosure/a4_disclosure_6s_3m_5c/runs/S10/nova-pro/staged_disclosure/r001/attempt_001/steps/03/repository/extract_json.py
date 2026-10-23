import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def extract_json(text):
    model_id = 'amazon.titan-text-express-v1'
    accept = 'application/json'
    content_type = 'application/json'

    body = {
        'inputText': text,
        'textGenerationConfig': {
            'maxTokenCount': 4096,
            'temperature': 0,
            'topP': 0.9
        }
    }

    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    result = json.loads(response.get('body').read())
    return result.get('results')[0].get('outputText')