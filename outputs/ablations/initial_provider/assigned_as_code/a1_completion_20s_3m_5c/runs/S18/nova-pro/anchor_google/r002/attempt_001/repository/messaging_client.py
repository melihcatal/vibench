import boto3


def get_sns_client():
    return boto3.client('sns', region_name='us-west-2')


def get_sqs_client():
    return boto3.client('sqs', region_name='us-west-2')