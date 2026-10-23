import boto3
import os

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

def message_summary(message):
    response = bedrock.invoke_model(modelId='amazon.titan-text-express-v1', body=message)
    return response