import boto3
import json

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

def invoke_model(model_id, body, accept='application/json', content_type='application/json'):
    response = bedrock_runtime.invoke_model(modelId=model_id, accept=accept, contentType=content_type, body=json.dumps(body))
    return json.loads(response['body'].read())

def invoke_model_with_response_stream(model_id, body, accept='application/json', content_type='application/json'):
    response = bedrock_runtime.invoke_model_with_response_stream(modelId=model_id, accept=accept, contentType=content_type, body=json.dumps(body))
    for event in response['body']['events']:
        if 'chunk' in event:
            yield event['chunk']