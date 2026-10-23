import os
import boto3

os.environ['AWS_ACCESS_KEY_ID'] = 'your_access_key_id'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_secret_access_key'

def summarize_message(message):
    client = boto3.client('bedrock-runtime', region_name='us-west-2')
    response = client.invoke_model(
        modelId='amazon.titan-text-express-v1',
        body=message
    )
    return response['body'].read()