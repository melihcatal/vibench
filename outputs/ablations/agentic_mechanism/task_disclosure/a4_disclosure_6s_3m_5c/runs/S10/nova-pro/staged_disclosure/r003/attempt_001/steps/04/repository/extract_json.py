import boto3

def extract_json(text):
    bedrock_client = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-text-express-v1'
    payload = {
        'inputText': text,
        'textGenerationConfig': {
            'maxTokenCount': 512,
            'temperature': 0.5,
            'topP': 0.9
        }
    }
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=payload
    )
    result = json.loads(response['body'].read())
    return result['results'][0]['outputText']