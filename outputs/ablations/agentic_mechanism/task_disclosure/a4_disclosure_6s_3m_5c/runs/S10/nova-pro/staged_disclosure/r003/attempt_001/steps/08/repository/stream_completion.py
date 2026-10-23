import boto3
import json

def stream_completion(prompt):
    bedrock = boto3.client('bedrock-runtime')
    body = json.dumps({"prompt": prompt, "max_tokens": 50})
    model_id = 'amazon.bedrock.claude-v2'
    accept = 'application/json'
    content_type = 'application/json'

    response = bedrock.invoke_model(body=body, modelId=model_id, accept=accept, contentType=content_type)
    response_body = json.loads(response.get('body').read())

    for token in response_body['completion']:
        yield token

if __name__ == '__main__':
    prompt = 'Translate the following English text to French: Hello, how are you?'
    for token in stream_completion(prompt):
        print(token, end='', flush=True)