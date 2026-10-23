import boto3


def get_sns_client():
    return boto3.client("sns")


def get_sqs_client():
    return boto3.client("sqs")
