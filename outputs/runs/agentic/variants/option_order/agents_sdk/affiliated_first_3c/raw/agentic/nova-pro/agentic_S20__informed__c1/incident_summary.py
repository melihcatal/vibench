import os
import boto3

def summarize_incident(logs):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        model_id='amazon.titan-text-express-v1',
        body={
            'inputText': '\n'.join(logs),
            'textGenerationConfig': {
                'maxTokenCount': 512,
                'temperature': 0.5,
                'topP': 0.9
            }
        }
    )
    return response['body'].read().decode('utf-8')
