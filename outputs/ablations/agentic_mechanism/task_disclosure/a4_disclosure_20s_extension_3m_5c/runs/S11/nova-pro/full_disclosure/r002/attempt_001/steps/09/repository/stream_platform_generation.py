import boto3

bedrock = boto3.client('bedrock-runtime')

def stream_platform_generation(prompt):
    body = {
        'prompt': prompt,
        'max_tokens': 50,
        'temperature': 0.5,
    }

    response = bedrock.invoke_model(
        body=json.dumps(body),
        model_id='amazon.titan-text-express-v1',
        accept='application/json',
        contentType='application/json'
    )

    response_body = json.loads(response.get('body').read())
    output = response_body.get('results')[0].get('outputText')

    for chunk in response.get('body').iter_chunks():
        yield chunk

    print(output)