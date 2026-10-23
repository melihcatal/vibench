import os
from typing import Optional


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.environ.get(
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
    "https://YOUR_RESOURCE.cognitiveservices.azure.com/",
)
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")

GOOGLE_APPLICATION_CREDENTIALS_PATH = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS", ""
)
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY", "")
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"

PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY", "")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def get_aws_session():
    import boto3
    from botocore.config import Config

    config = Config(
        region_name=AWS_DEFAULT_REGION,
        retries={"max_attempts": 3, "mode": "standard"},
    )
    return boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION,
    ), config


def get_azure_document_client():
    from azure.ai.formrecognizer import DocumentAnalysisClient
    from azure.core.credentials import AzureKeyCredential

    credential = AzureKeyCredential(AZURE_DOCUMENT_INTELLIGENCE_KEY)
    client = DocumentAnalysisClient(
        endpoint=AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT,
        credential=credential,
    )
    return client


def get_google_document_ai_client():
    from google.cloud import documentai_v1 as documentai

    project_id = GOOGLE_CLOUD_PROJECT
    location = "us"
    return documentai.DocumentProcessorServiceClient(), project_id, location


def get_openai_client():
    import openai

    client = openai.OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
    )
    return client


def get_deepl_session():
    import httpx

    return httpx.Client(
        base_url=DEEPL_API_URL,
        headers={"Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"},
    )


def get_perspective_session():
    import httpx

    return httpx.Client(
        base_url=PERSPECTIVE_API_URL,
    )
