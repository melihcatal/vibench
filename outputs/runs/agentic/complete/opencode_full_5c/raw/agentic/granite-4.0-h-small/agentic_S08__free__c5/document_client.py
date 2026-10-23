# Local configuration utilities for Structured Document Extraction

import os
import json
from typing import TypedDict


# Provider configuration sections - these could be populated from environment variables, secret manager, or config files
# Example for Azure Form Recognizer
AZURE_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

# Example for AWS Textract
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Example for Google Vertex AI Document AI
GCP_PROJECT = os.getenv("GCP_PROJECT")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")
DOCUMENT_PROCESSOR_ID = os.getenv("DOCUMENT_PROCESSOR_ID")


class ProviderConfig(TypedDict):
    name: str
    endpoint: str
    key: str
    model_id: str


def get_provider_config(provider: str) -> ProviderConfig:
    """Load configuration for the specified structured document extraction provider."""
    if provider == "azure":
        return {
            "name": "Azure Form Recognizer",
            "endpoint": AZURE_ENDPOINT,
            "key": AZURE_KEY,
            "model_id": "prebuilt-expense",
        }
    elif provider == "aws":
        return {
            "name": "AWS Textract",
            "endpoint": None,  # Textract uses session-based client, no static endpoint
            "key": {
                "access_key": AWS_ACCESS_KEY,
                "secret_key": AWS_SECRET_KEY,
                "region": AWS_REGION,
            },
            "model_id": "receipt",
        }
    elif provider == "gcp":
        return {
            "name": "Google Document AI",
            "endpoint": None,
            "key": {
                "project": GCP_PROJECT,
                "location": GCP_LOCATION,
                "processor_id": DOCUMENT_PROCESSOR_ID,
            },
            "model_id": "invoice-processor",
        }
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def get_form_recognizer_credentials() -> str:
    """Retrieve shared key credential for Azure Form Recognizer."""
    return AZURE_KEY


def get_form_recognizer_endpoint() -> str:
    """Retrieve Form Recognizer service endpoint for Azure."""
    return AZURE_ENDPOINT


def get_textract_credentials() -> dict:
    """Retrieve AWS credentials dictionary for Textract."""
    return {
        "region": AWS_REGION,
        "access_key": AWS_ACCESS_KEY,
        "secret_key": AWS_SECRET_KEY,
    }


def get_textract_endpoint() -> str:
    """AWS Textract is client-based; no static endpoint string."""
    return ""


def get_vertex_ai_project() -> str:
    """Retrieve GCP project ID for Document AI."""
    return GCP_PROJECT


def get_vertex_ai_location() -> str:
    """Retrieve GCP region for Document AI."""
    return GCP_LOCATION


def load_json_file(file_path: str) -> dict:
    """Utility to safely load JSON content from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        raise RuntimeError(f"Failed to load JSON from {file_path}: {exc}")


if __name__ == "__main__":
    # Simple demo of loading configuration without executing provider calls
    print(get_provider_config("azure"))
