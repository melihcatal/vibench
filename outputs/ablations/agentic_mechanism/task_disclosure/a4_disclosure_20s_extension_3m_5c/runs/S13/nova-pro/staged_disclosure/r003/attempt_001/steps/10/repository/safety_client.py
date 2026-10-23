import os
import boto3

BEDROCK_REGION = 'us-east-1'

def get_bedrock_client():
    return boto3.client('bedrock', region_name=BEDROCK_REGION)

def get_text_content_safety_model_id():
    return 'amazon.bedrock.content-safety.v1'