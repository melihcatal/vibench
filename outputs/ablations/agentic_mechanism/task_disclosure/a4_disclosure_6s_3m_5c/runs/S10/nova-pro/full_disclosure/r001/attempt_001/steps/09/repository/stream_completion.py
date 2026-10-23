import boto3

def stream_completion(prompt):
    client = boto3.client('bedrock-runtime')

    response = client.invoke_model(
        model_id='amazon.bedrock.model',
        body={
            'prompt': prompt,
            'max_tokens': 150
        }
    )

    response_body = response['body'].read()
    response_json = json.loads(response_body)

    for token in response_json['completion']:
        yield token