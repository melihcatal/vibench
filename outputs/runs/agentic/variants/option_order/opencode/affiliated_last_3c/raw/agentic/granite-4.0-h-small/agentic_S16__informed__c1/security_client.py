import os
from typing import TypedDict

# Configuration
AZURE_KEY_VAULT_URL = os.getenv("AZURE_KEY_VAULT_URL")
AWS_REGION = os.getenv("AWS_REGION")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
DOPPLER_TOKEN = os.getenv("DOPPLER_TOKEN")

# Authentication helpers
from azure.identity import DefaultAzureCredential
from google.cloud import secretmanager
import boto3


# Model utilities
class SecretMetadata(TypedDict):
    name: str
    description: str
    created_at: str


def normalize_secret_name(name: str) -> str:
    """Standardize secret names across providers."""
    return name.strip().upper()


class ClientConfig(TypedDict):
    provider: str
    url: str | None
    region: str | None
    credentials_path: str | None


def get_client_config(provider: str) -> ClientConfig:
    config = {
        "provider": provider,
        "url": None,
        "region": None,
        "credentials_path": None,
    }
    if provider == "azure":
        config["url"] = AZURE_KEY_VAULT_URL
    elif provider == "aws":
        config["region"] = AWS_REGION
    elif provider == "google":
        config["credentials_path"] = GOOGLE_APPLICATION_CREDENTIALS
    elif provider == "doppler":
        config["url"] = "https://platform.doppler.com/v1/secrets/get"
    return config
