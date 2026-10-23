import boto3
import json

def answer_with_context(question, context):
    client = boto3.client('bedrock-runtime')
    model_id = 'amazon.titan-text-express-v1'
    body = {
        'inputText': f'{context} Question: {question}',
        'textGenerationConfig': {
            'maxTokenCount': 512,
            'temperature': 0.5,
            'topP': 0.9
        }
    }
    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(body)
    )
    result = json.loads(response['body'].read())
    return result['results'][0]['outputText']