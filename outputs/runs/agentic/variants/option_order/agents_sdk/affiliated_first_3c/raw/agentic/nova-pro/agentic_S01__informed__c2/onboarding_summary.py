import os
import boto3

def summarize_text(text):
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    model_id = 'amazon.titan-text-express-v1'
    response = client.invoke_model(
        modelId=model_id,
        body={
            'inputText': text,
            'textGenerationConfig': {
                'maxTokenCount': 512,
                'temperature': 0.5,
                'topP': 0.9
            }
        }
    )
    return response['body'].read().decode('utf-8')