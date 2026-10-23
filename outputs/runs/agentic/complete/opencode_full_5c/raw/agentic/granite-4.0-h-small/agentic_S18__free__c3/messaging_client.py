import json

# [HELPER] messaging_client.py
# Helper utilities to obtain configured AWS clients for SNS and SQS

import boto3


def get_sns_client() -> boto3.client:
    """Create and return an SNS client with default credentials and region."""
    return boto3.client("sns", region_name="us-east-1")


def get_sqs_client() -> boto3.client:
    """Create and return an SQS client with default credentials and region."""
    return boto3.client("sqs", region_name="us-east-1")
