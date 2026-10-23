import os
import boto3
from openai import OpenAI


def get_kms_client():
    return boto3.client("kms")


def get_cloudwatch_client():
    return boto3.client("cloudwatch")


def get_translate_client():
    return boto3.client("translate")


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return OpenAI(api_key=api_key)
