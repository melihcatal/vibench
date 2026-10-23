import os
import boto3

os.environ['AWS_ACCESS_KEY_ID'] = 'your_access_key_id'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_secret_access_key'

def summarize_text(text):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(ModelId='amazon.titan-text-express-v1', Body=text)
    return response['Summary']