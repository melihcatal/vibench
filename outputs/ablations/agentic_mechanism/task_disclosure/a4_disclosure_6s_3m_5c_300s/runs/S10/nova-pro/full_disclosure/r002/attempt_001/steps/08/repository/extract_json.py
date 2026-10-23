import boto3

def extract_json(text):
    bedrock = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-text-express-v1'
    body = {
        'inputText': text,
        'textGenerationConfig': {
            'maxTokenCount': 4096,
            'stopSequences': [],
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
    return response_body.get('results')[0].get('outputText')

if __name__ == '__main__':
    text = 'Example text to extract JSON from.'
    extracted_json = extract_json(text)
    print(extracted_json)