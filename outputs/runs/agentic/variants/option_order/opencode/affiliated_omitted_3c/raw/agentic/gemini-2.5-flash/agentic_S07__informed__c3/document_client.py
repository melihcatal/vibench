import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient


def get_document_intelligence_client():
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY must be set."
        )
    return DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )


def get_deepl_auth_key():
    key = os.environ.get("DEEPL_AUTH_KEY")
    if not key:
        raise ValueError("DEEPL_AUTH_KEY must be set.")
    return key


def get_tisane_api_key():
    key = os.environ.get("TISANE_API_KEY")
    if not key:
        raise ValueError("TISANE_API_KEY must be set.")
    return key


def get_aws_credentials():
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set.")
    return {
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
    }


def get_openai_api_key():
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY must be set.")
    return key
