import boto3

bedrock = boto3.client('bedrock-runtime')

model_id = 'amazon.titan-text-express-v1'

def stream_text(prompt):
    body = {
        'inputText': prompt,
        'textGenerationConfig': {
            'maxTokenCount': 512,
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

    for char in output_text:
        yield char

if __name__ == '__main__':
    prompt = 'Once upon a time,'
    for char in stream_text(prompt):
        print(char, end='', flush=True)