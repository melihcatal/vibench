import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def invoke_model(model_id, prompt, max_tokens):
    body = {
        'prompt': prompt,
        'max_tokens_to_sample': max_tokens
    }
    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    return json.loads(response.get('body').read())

def invoke_model_with_response_stream(model_id, prompt, max_tokens):
    body = {
        'prompt': prompt,
        'max_tokens_to_sample': max_tokens
    }
    response = bedrock.invoke_model_with_response_stream(
        body=json.dumps(body),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    return response.get('body')