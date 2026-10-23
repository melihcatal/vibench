import boto3

bedrock = boto3.client('bedrock', region_name='us-east-1')

def extract_json(text):
    model_id = 'amazon.titan-tg1-large'
    accept = 'application/json'
    content_type = 'application/json'

    body = {
        'inputText': text,
        'textGenerationConfig': {
            'maxTokenCount': 4096,
            'temperature': 0.5,
            'topP': 0.9
        }
    }

    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    response_body = response['body'].read()
    response_json = json.loads(response_body)

    return response_json