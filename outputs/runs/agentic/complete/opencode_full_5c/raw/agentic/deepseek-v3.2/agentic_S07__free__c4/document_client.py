import os
from typing import Optional
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()


class DocumentClientConfig:
    """Configuration for document analysis clients."""

    def __init__(self):
        self.azure_endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
        self.azure_key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")

    def validate_azure_config(self) -> bool:
        """Validate Azure Form Recognizer configuration."""
        return bool(self.azure_endpoint and self.azure_key)

    def validate_openai_config(self) -> bool:
        """Validate OpenAI configuration."""
        return bool(self.openai_api_key)

    def validate_google_config(self) -> bool:
        """Validate Google Cloud configuration."""
        return bool(self.google_api_key)

    def validate_aws_config(self) -> bool:
        """Validate AWS configuration."""
        return bool(self.aws_access_key and self.aws_secret_key)


def get_azure_client() -> DocumentAnalysisClient:
    """Get Azure Form Recognizer client."""
    config = DocumentClientConfig()
    if not config.validate_azure_config():
        raise ValueError(
            "Azure Form Recognizer configuration missing. "
            "Set AZURE_FORM_RECOGNIZER_ENDPOINT and AZURE_FORM_RECOGNIZER_KEY environment variables."
        )

    credential = AzureKeyCredential(config.azure_key)
    client = DocumentAnalysisClient(
        endpoint=config.azure_endpoint, credential=credential
    )
    return client


def get_openai_client():
    """Get OpenAI client."""
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "OpenAI package not installed. Install with: pip install openai"
        )

    config = DocumentClientConfig()
    if not config.validate_openai_config():
        raise ValueError(
            "OpenAI configuration missing. Set OPENAI_API_KEY environment variable."
        )

    client = OpenAI(api_key=config.openai_api_key, base_url=config.openai_base_url)
    return client


def get_google_client():
    """Get Google Cloud client for translation."""
    try:
        from google.cloud import translate_v2 as translate
    except ImportError:
        raise ImportError(
            "Google Cloud Translate package not installed. Install with: pip install google-cloud-translate"
        )

    config = DocumentClientConfig()
    if not config.validate_google_config():
        raise ValueError(
            "Google Cloud configuration missing. "
            "Set GOOGLE_API_KEY environment variable."
        )

    client = translate.Client()
    return client


def get_aws_client(service_name: str):
    """Get AWS client for specified service."""
    try:
        import boto3
    except ImportError:
        raise ImportError(
            "boto3 package not installed. Install with: pip install boto3"
        )

    config = DocumentClientConfig()
    if not config.validate_aws_config():
        raise ValueError(
            "AWS configuration missing. "
            "Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )

    client = boto3.client(
        service_name,
        aws_access_key_id=config.aws_access_key,
        aws_secret_access_key=config.aws_secret_key,
        region_name=config.aws_region,
    )
    return client
