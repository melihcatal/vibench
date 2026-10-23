import os
import boto3

AWS_REGION = 'us-west-2'
BEDROCK_CLIENT = boto3.client('bedrock-runtime', region_name=AWS_REGION)

def get_model_families():
    response = BEDROCK_CLIENT.list_foundation_models()
    return response['modelSummaries']

def invoke_model(model_id, prompt):
    body = {
        'prompt': prompt,
        'max_tokens': 150,
        'temperature': 0.7
    }
    response = BEDROCK_CLIENT.invoke_model(
        modelId=model_id,
        body=json.dumps(body)
    )
    return json.loads(response['body'].read())['outputs'][0]['text']