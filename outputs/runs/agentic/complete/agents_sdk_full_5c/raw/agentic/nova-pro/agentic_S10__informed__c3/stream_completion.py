import os
import boto3

client = boto3.client('bedrock-runtime', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def stream_completion(prompt):
    response = client.invoke_model(
        modelId='amazon.titan-text-express-v1',
        body={'inputText': prompt, 'textGenerationConfig': {'maxTokenCount': 500, 'stopSequences': [], 'temperature': 0.5, 'topP': 0.9}}
    )
    for event in response['body']['chunks']:
        yield event['text']