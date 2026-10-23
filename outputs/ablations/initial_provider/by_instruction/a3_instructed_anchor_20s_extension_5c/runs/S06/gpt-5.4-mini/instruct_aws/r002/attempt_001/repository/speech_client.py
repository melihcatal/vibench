import os
import boto3
from botocore.config import Config


def get_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def get_polly_client():
    return boto3.client("polly", region_name=get_region(), config=Config(retries={"max_attempts": 3, "mode": "standard"}))


def get_default_voice_map():
    return {
        "en-US": ["Joanna", "Matthew", "Ivy", "Kendra", "Kimberly"],
        "en-GB": ["Amy", "Brian", "Emma"],
        "es-ES": ["Lucia", "Sergio"],
        "fr-FR": ["Celine", "Lea", "Mathieu"],
    }
