import boto3
import json

bedrock = boto3.client('bedrock-runtime')

def answer_with_context(question, context):
    payload = {
        'prompt': f'{context} Question: {question}',
        'max_tokens': 150
    }
    response = bedrock.invoke_model(
        model_id='amazon.titan-text-express-v1',
        body=json.dumps(payload)
    )
    return parse_response(response)['outputText']