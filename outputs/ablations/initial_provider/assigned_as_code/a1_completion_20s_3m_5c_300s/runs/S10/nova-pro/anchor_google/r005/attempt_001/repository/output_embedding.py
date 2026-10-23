import boto3
import json

bedrock = boto3.client('bedrock-runtime')

def embed_output(text):
    payload = {
        'text': text
    }
    response = bedrock.invoke_model(
        model_id='amazon.titan-text-embed-v1',
        body=json.dumps(payload)
    )
    return parse_response(response)['embedding']