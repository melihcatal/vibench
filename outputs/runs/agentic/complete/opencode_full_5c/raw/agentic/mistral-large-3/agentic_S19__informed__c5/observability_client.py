import os
from typing import Dict, Any, Union
from google.cloud import monitoring_v3, storage
from google.oauth2 import service_account
from openai import OpenAI
from anthropic import Anthropic
import boto3
from ibm_watsonx_ai import APIClient
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def get_client(service_type: str, client_class: Any = None) -> Any:
    """
    Provides a configured client for the specified service using environment variables.

    Args:
        service_type: The type of service (e.g., "monitoring", "storage", "openai", "anthropic", "watsonx").
        client_class: The client class to instantiate if applicable.

    Returns:
        A configured client instance.
    """
    if service_type == "monitoring":
        credentials = service_account.Credentials.from_service_account_file(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
        return client_class(credentials=credentials)

    elif service_type == "storage":
        credentials = service_account.Credentials.from_service_account_file(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        )
        return client_class(credentials=credentials)

    elif service_type == "openai":
        return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    elif service_type == "anthropic":
        return Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    elif service_type == "watsonx":
        authenticator = IAMAuthenticator(os.getenv("WATSONX_API_KEY"))
        client = APIClient(authenticator=authenticator)
        client.set_service_url(
            os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        )
        return client

    elif service_type == "aws":
        return boto3.client(
            service_name=client_class,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    else:
        raise ValueError(f"Unsupported service type: {service_type}")
