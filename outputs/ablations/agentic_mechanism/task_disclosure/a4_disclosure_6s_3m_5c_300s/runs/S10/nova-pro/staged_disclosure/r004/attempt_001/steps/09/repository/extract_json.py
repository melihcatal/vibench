import boto3

bedrock = boto3.client(service_name='bedrock', region_name='us-east-1')

def extract_json(text):
    model_id = 'amazon.titan-text-lite-v1'
    accept = 'application/json'
    content_type = 'application/json'

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
        accept=accept,
        contentType=content_type
    )

    response_body = json.loads(response.get('body').read())
    output_text = response_body.get('results')[0].get('outputText')

    return json.loads(output_text)

if __name__ == '__main__'):
    text = 'Your input text goes here'
    extracted_json = extract_json(text)
    print(extracted_json)