import boto3
import json

bedrock = boto3.client('bedrock-runtime')

def check_safety(text):
    payload = {
        'text': text
    }
    response = bedrock.invoke_model(
        model_id='amazon.titan-text-safety-v1',
        body=json.dumps(payload)
    )
    return parse_response(response)['isSafe']