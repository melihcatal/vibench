import boto3
import json

bedrock = boto3.client('bedrock-runtime')

def translate_result(text, target_language):
    payload = {
        'text': text,
        'target_language': target_language
    }
    response = bedrock.invoke_model(
        model_id='amazon.titan-text-translate-v1',
        body=json.dumps(payload)
    )
    return parse_response(response)['translatedText']