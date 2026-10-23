import os
import boto3
import openai
import deepl


def get_aws_secrets_manager_client():
    return boto3.client(
        "secretsmanager",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION"),
    )


def get_openai_client():
    return openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_deepl_translator():
    return deepl.Translator(auth_key=os.environ.get("DEEPL_AUTH_KEY"))


def get_azure_content_safety_config():
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    return endpoint, key
