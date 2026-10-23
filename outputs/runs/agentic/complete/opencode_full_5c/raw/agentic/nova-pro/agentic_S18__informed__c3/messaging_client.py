import boto3


# Provide local configuration and client helper utilities for Pub/Sub Messaging
def get_sns_client():
    return boto3.client("sns")


def get_sqs_client():
    return boto3.client("sqs")
