import os
import boto3


def get_sns_client():
    return boto3.client('sns', region_name=os.getenv('AWS_REGION'))


def get_sqs_client():
    return boto3.client('sqs', region_name=os.getenv('AWS_REGION'))