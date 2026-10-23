import os
import boto3
import openai

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def get_kms_client():
    return boto3.client("kms", region_name=AWS_REGION)


def get_cloudwatch_client():
    return boto3.client("cloudwatch", region_name=AWS_REGION)


def get_translate_client():
    return boto3.client("translate", region_name=AWS_REGION)


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY required")
    return openai.OpenAI(api_key=api_key)
