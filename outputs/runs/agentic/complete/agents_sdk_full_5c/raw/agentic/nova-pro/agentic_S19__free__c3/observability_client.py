import os
import boto3

def get_cloudwatch_client():
    return boto3.client('cloudwatch', region_name=os.getenv('AWS_REGION'))

def get_translate_client():
    return boto3.client('translate', region_name=os.getenv('AWS_REGION'))

def get_comprehend_client():
    return boto3.client('comprehend', region_name=os.getenv('AWS_REGION'))

def get_s3_client():
    return boto3.client('s3', region_name=os.getenv('AWS_REGION'))