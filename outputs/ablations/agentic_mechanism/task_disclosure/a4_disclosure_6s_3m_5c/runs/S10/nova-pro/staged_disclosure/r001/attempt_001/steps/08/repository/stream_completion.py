import boto3

bedrock = boto3.client('bedrock-runtime')

def stream_completion(prompt):
    body = {
        "prompt": prompt,
        "max_tokens": 50,
        "temperature": 0.5
    }

    model_id = 'amazon.titan-text-express-v1'
    response = bedrock.invoke_model(body=json.dumps(body), modelId=model_id, accept='application/json', contentType='application/json')

    response_body = json.loads(response.get('body').read())
    output = response_body.get('results')[0].get('outputText')
    yield output

if __name__ == '__main__':
    prompt = 'Once upon a time,'
    for token in stream_completion(prompt):
        print(token, end='', flush=True)