import os
import boto3
import cohere
import deepl
import openai
from google.cloud import kms
from azure.keyvault.keys.crypto import CryptographyClient
from azure.identity import DefaultAzureCredential


def get_aws_kms_client():
    return boto3.client("kms", region_name=os.environ.get("AWS_REGION", "us-east-1"))


def get_gcp_kms_client():
    return kms.KeyManagementServiceClient()


def get_azure_crypto_client(key_id: str):
    credential = DefaultAzureCredential()
    return CryptographyClient(key_id, credential=credential)


def get_aws_cloudtrail_client():
    return boto3.client(
        "cloudtrail", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )


def get_openai_client():
    return openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_cohere_client():
    return cohere.Client(os.environ.get("COHERE_API_KEY"))


def get_deepl_translator():
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    return deepl.Translator(auth_key)
