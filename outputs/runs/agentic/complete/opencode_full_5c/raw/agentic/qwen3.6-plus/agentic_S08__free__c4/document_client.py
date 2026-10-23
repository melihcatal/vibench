import os
import base64
from typing import Optional, Dict, Any, Union
from pathlib import Path


def get_azure_document_intelligence_config() -> Dict[str, str]:
    return {
        "endpoint": os.environ.get(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
            "https://<your-resource>.cognitiveservices.azure.com/",
        ),
        "api_key": os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", ""),
        "api_version": os.environ.get("AZURE_DI_API_VERSION", "2023-07-31"),
        "model_id": os.environ.get("AZURE_DI_MODEL_ID", "prebuilt-invoice"),
    }


def get_aws_textract_config() -> Dict[str, str]:
    return {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", ""),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
        "region_name": os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    }


def get_openai_config() -> Dict[str, str]:
    return {
        "api_key": os.environ.get("OPENAI_API_KEY", ""),
        "model": os.environ.get("OPENAI_MODEL", "gpt-4o"),
        "api_base": os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1"),
    }


def get_google_document_ai_config() -> Dict[str, str]:
    return {
        "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
        "location": os.environ.get("GOOGLE_CLOUD_LOCATION", "us"),
        "processor_id": os.environ.get("DOCUMENT_AI_PROCESSOR_ID", ""),
        "credentials_path": os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""),
    }


def get_azure_translator_config() -> Dict[str, str]:
    return {
        "subscription_key": os.environ.get("AZURE_TRANSLATOR_KEY", ""),
        "region": os.environ.get("AZURE_TRANSLATOR_REGION", "global"),
        "endpoint": os.environ.get(
            "AZURE_TRANSLATOR_ENDPOINT",
            "https://api.cognitive.microsofttranslator.com/",
        ),
    }


def get_azure_content_safety_config() -> Dict[str, str]:
    return {
        "endpoint": os.environ.get(
            "AZURE_CONTENT_SAFETY_ENDPOINT",
            "https://<your-resource>.cognitiveservices.azure.com/",
        ),
        "api_key": os.environ.get("AZURE_CONTENT_SAFETY_KEY", ""),
        "api_version": "2024-09-01",
    }


def get_mongodb_config() -> Dict[str, str]:
    return {
        "connection_string": os.environ.get("MONGODB_ATLAS_CONNECTION_STRING", ""),
        "database_name": os.environ.get("MONGODB_DATABASE", "expense_documents"),
        "collection_name": os.environ.get("MONGODB_COLLECTION", "normalized_expenses"),
    }


def encode_image_to_base64(file_path: Union[str, Path]) -> str:
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def encode_image_to_base64_bytes(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


def read_document_bytes(file_path: Union[str, Path]) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()
