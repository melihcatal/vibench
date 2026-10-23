import boto3

def extract_json(text):
    bedrock = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-text-express-v1'
    payload = {
        'inputText': text,
        'textGenerationConfig': {
            'maxTokenCount': 4096,
            'temperature': 0,
            'topP': 0.9
        }
    }
    response = bedrock.invoke_model(
        body=json.dumps(payload),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    result = json.loads(response['body'].read())
    return result.get('outputText', '')

if __name__ == '__main__':\n    text = 'Sample text to extract JSON from.'
    extracted_json = extract_json(text)
    print(extracted_json)