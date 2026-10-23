import boto3

def stream_completion(model_id, prompt):
    bedrock_runtime = boto3.client('bedrock-runtime')

    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        body={
            'prompt': prompt,
            'max_tokens': 150,
            'temperature': 0.7
        }
    )

    response_body = response['body'].read()
    response_json = json.loads(response_body)

    for token in response_json['completion']:
        yield token

if __name__ == '__main__':
    model_id = 'amazon.titan-text-express-v1'
    prompt = 'Once upon a time,'
    for token in stream_completion(model_id, prompt):
        print(token, end='', flush=True)