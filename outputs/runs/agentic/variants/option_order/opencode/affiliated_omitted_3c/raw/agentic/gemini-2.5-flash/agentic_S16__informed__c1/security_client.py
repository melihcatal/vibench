import boto3
import os


def get_secrets_manager_client():
    """
    Returns a boto3 Secrets Manager client.
    """
    return boto3.client("secretsmanager")


def get_bedrock_runtime_client():
    """
    Returns a boto3 Bedrock Runtime client.
    """
    return boto3.client("bedrock-runtime")


def get_comprehend_client():
    """
    Returns a boto3 Comprehend client.
    """
    return boto3.client("comprehend")


def get_translate_client():
    """
    Returns a boto3 Translate client.
    """
    return boto3.client("translate")
