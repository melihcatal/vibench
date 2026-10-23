import os

# Shared configuration utilities
SECRET_VAULT = os.getenv(
    "SECRET_VAULT", "azure"
)  # Options: azure, aws, gcp, alibaba, doppler


class SecurityClient:
    """Local helper for initializing provider-specific secret management clients."""

    def __init__(self):
        if SECRET_VAULT == "azure":
            from azure.identity import DefaultAzureCredential
            from azure.keyvault.secrets import SecretClient

            self.client = SecretClient(
                vault_url=os.getenv("AZURE_KEY_VAULT_URL"),
                credential=DefaultAzureCredential(),
            )
        elif SECRET_VAULT == "aws":
            import boto3

            self.client = boto3.client(
                service_name="secretsmanager",
                region_name=os.getenv("AWS_REGION", "us-east-1"),
            )
        elif SECRET_VAULT == "gcp":
            from google.cloud import secretmanager

            self.client = secretmanager.SecretManagerServiceClient()
        elif SECRET_VAULT == "alibaba":
            from alibabacloud_kms20201212.client import Client as KmsClient
            from alibabacloud_tea_openapi.models import Config

            config = Config(
                access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
                access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
                region_id=os.getenv("ALIBABA_CLOUD_REGION", "cn-hangzhou"),
            )
            self.client = KmsClient(config)
        elif SECRET_VAULT == "doppler":
            import requests

            self.client = requests.Session()
            self.client.headers.update(
                {"Authorization": f"Bearer {os.getenv('DOPPLER_TOKEN')}"}
            )
        else:
            raise ValueError(f"Unsupported SECRET_VAULT: {SECRET_VAULT}")
