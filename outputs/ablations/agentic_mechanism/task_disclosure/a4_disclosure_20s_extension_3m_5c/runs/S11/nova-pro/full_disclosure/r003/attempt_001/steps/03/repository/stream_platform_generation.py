import boto3

bedrock = boto3.client('bedrock-runtime')

def stream_platform_generation(prompt):
    body = {
        'inputText': prompt,
        'textGenerationConfig': {
            'maxTokenCount': 512,
            'stopSequences': [],
            'temperature': 0.5,
            'topP': 0.9
        }
    }

    modelId = 'amazon.titan-text-express-v1'
    accept = 'application/json'
    contentType = 'application/json'

    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=modelId,
        accept=accept,
        contentType=contentType
    )

    response_body = json.loads(response.get('body').read())
    outputText = response_body.get('results')[0].get('outputText')

    for chunk in outputText.split():  # Simulate streaming
        yield chunk

if __name__ == '__main__':
    prompt = 'Once upon a time'
    for chunk in stream_platform_generation(prompt):
        print(chunk, end='', flush=True)