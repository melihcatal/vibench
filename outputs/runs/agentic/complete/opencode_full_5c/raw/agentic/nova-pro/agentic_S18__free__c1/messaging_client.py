import boto3


def get_sqs_client():
    return boto3.client("sqs")


def get_sns_client():
    return boto3.client("sns")
