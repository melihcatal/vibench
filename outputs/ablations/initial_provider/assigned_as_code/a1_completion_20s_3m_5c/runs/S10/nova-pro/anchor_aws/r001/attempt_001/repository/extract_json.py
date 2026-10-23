import boto3

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def extract_json(text):
    model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
    body = {
        'prompt': f'Extract JSON from the following text: {text}',
        'max_tokens_to_sample': 300
    }
    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    response_body = json.loads(response.get('body').read())
    return response_body.get('completions')[0].get('data').get('text')