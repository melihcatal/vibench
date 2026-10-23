import os
import boto3

def get_bedrock_client():
    return boto3.client('bedrock-runtime', region_name='us-west-2')

def get_comprehend_client():
    return boto3.client('comprehend')