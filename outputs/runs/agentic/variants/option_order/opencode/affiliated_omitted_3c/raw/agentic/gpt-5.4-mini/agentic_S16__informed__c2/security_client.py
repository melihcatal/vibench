import os
import boto3


def get_secret_manager_client():
    return boto3.client("secretsmanager")


def resolve_secret_name(env_name: str, default: str) -> str:
    return os.getenv(env_name, default)
