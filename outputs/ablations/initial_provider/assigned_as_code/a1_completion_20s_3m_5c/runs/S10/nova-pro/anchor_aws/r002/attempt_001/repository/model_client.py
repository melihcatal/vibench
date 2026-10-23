import boto3
import json

bedrock = boto3.client('bedrock-runtime')

def invoke_model(model_id, body):
    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    return json.loads(response.get('body').read())