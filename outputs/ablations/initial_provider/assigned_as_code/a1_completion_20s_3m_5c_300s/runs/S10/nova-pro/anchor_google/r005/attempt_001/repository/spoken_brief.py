import boto3
import json

bedrock = boto3.client('bedrock-runtime')

def generate_spoken_brief(text):
    payload = {
        'text': text
    }
    response = bedrock.invoke_model(
        model_id='amazon.titan-text-to-speech-v1',
        body=json.dumps(payload)
    )
    return parse_response(response)['audio']