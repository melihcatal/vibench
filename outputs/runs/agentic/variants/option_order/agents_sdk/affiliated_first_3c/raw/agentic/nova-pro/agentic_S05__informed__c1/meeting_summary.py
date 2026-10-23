import os
import boto3

def summarize_meeting(transcript):
    bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
    response = bedrock.invoke_model(ModelId='amazon.titan-text-express-v1', Body=transcript)
    return response['Body'].read().decode('utf-8')