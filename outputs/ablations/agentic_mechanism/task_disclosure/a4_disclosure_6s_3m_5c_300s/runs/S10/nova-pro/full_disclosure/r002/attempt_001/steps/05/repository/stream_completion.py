import boto3

def stream_completion(prompt, model_id='amazon.titan-text-express-v1'):
    client = boto3.client('bedrock-runtime')

    response = client.invoke_model(
        modelId=model_id,
        body={
            'prompt': prompt,
            'maxTokens': 500,
            'temperature': 0.5
        }
    )

    response_body = response['body'].read()
    response_json = json.loads(response_body)

    for token in response_json['completion']:
        yield token