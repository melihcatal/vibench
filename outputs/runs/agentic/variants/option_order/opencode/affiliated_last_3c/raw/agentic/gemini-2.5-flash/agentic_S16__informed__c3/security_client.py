import boto3
import os
from google.cloud import secretmanager_v1beta1 as secretmanager
from google.cloud import translate_v2 as translate
import google.generativeai as genai


def get_aws_secrets_manager_client():
    return boto3.client(
        "secretsmanager",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )


def get_google_secret_manager_client():
    return secretmanager.SecretManagerServiceClient()


def get_gemini_model(model_name: str):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return genai.GenerativeModel(model_name)


def get_google_translate_client():
    return translate.Client()
