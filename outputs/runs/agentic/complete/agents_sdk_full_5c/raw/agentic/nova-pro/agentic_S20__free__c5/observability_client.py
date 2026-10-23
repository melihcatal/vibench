import os
import boto3

CLOUDWATCH_LOGS = boto3.client('logs', region_name=os.getenv('AWS_REGION'))
COMPREHEND = boto3.client('comprehend', region_name=os.getenv('AWS_REGION'))
SAGEMAKER = boto3.client('sagemaker', region_name=os.getenv('AWS_REGION'))