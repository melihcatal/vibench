import os
from typing import Any, Dict, Optional


class SecretClientWrapper:
    """Local helper that abstracts the concrete secret manager SDK / REST client.
    Concrete provider configuration is loaded from environment variables.",

    # Provider signals (must be present in the environment):
    #   AZURE_KEY_VAULT_URL, AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET
    #   AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
    #   IBM_SECRETS_MANAGER_APIKEY, IBM_CREDENTIALS_FILE
    #   GOOGLE_APPLICATION_CREDENTIALS
    #   ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET, ALIBABA_CLOUD_REGION
    #   DOPPLER_TOKEN
    """

    def __init__(self):
        self.provider = self._detect_provider()
        if self.provider == "azure":
            from azure.identity import DefaultAzureCredential
            from azure.keyvault.secrets import SecretClient

            credential = DefaultAzureCredential()
            self.client = SecretClient(
                vault_url=os.getenv("AZURE_KEY_VAULT_URL"), credential=credential
            )
        elif self.provider == "aws":
            import boto3

            self.client = boto3.client(
                "secretsmanager", region_name=os.getenv("AWS_REGION")
            )
        elif self.provider == "ibm":
            from ibm_secrets_manager_sdk import SecretsManagerV1

            service = SecretsManagerV1.new_instance(
                apikey=os.getenv("IBM_SECRETS_MANAGER_APIKEY")
            )
            self.client = service
        elif self.provider == "google":
            from google.cloud import secretmanager

            self.client = secretmanager.SecretManagerServiceClient()
        elif self.provider == "alibaba":
            from alibabacloud_kms20240708.client import Client as KMSClient

            # For simplicity, we reuse the KMS client for secret access; adjust as needed.
            self.client = KMSClient(
                access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
                access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
                region_id=os.getenv("ALIBABA_CLOUD_REGION"),
            )
        elif self.provider == "doppler":
            import requests

            self.doppler_token = os.getenv("DOPPLER_TOKEN")
            self.base_url = "https://api.doppler.com/v1/secrets"
        else:
            raise RuntimeError("Unsupported secret manager provider detected")

    def _detect_provider(self) -> str:
        """Detect provider based on which environment variables are set.
        Returns a short code string used in subsequent branches.
        """
        if all(
            k in os.environ
            for k in [
                "AZURE_KEY_VAULT_URL",
                "AZURE_TENANT_ID",
                "AZURE_CLIENT_ID",
                "AZURE_CLIENT_SECRET",
            ]
        ):
            return "azure"
        if all(
            k in os.environ
            for k in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_REGION"]
        ):
            return "aws"
        if "IBM_SECRETS_MANAGER_APIKEY" in os.environ:
            return "ibm"
        if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
            return "google"
        if all(
            k in os.environ
            for k in [
                "ALIBABA_CLOUD_ACCESS_KEY_ID",
                "ALIBABA_CLOUD_ACCESS_KEY_SECRET",
                "ALIBABA_CLOUD_REGION",
            ]
        ):
            return "alibaba"
        if "DOPPLER_TOKEN" in os.environ:
            return "doppler"
        raise RuntimeError(
            "No supported secret manager credentials found in environment"
        )

    def get_secret(self, name: str) -> Any:
        """Generic secret retrieval returning the raw value (string or dict)."""
        if self.provider == "azure":
            return self.client.get_secret(name).value
        elif self.provider == "aws":
            resp = self.client.get_secret_value(SecretId=name)
            # Secrets Manager returns a string or binary; decode if needed
            return (
                resp["SecretString"]
                if "SecretString" in resp
                else resp["SecretBinary"].decode()
            )
        elif self.provider == "ibm":
            resp = self.client.get_secret(name)
            return resp.get_result().get("secret")
        elif self.provider == "google":
            parent = f"projects/-/secrets/{name}/versions/latest"
            resp = self.client.access_secret_version(name=parent)
            return resp.payload.data.decode("UTF-8")
        elif self.provider == "alibaba":
            # Alibaba KMS API example; adjust payload handling in real usage
            response = self.client.get_secret(name)
            return response.body.getvalue()
        elif self.provider == "doppler":
            resp = requests.get(
                f"{self.base_url}/fetch",
                headers={"Authorization": f"Bearer {self.doppler_token}"},
                json={"name": name},
            )
            resp.raise_for_status()
            return resp.json()["value"]
        else:
            raise RuntimeError("Unsupported provider branch")

    def get_secret_version(self, name: str, version_id: str):
        """Retrieve a specific version of a secret (if supported)."""
        if self.provider == "azure":
            return self.client.get_secret(name, version=version_id).value
        elif self.provider == "aws":
            return self.client.get_secret_value(SecretId=name, VersionId=version_id)[
                "SecretString"
            ]
        else:
            raise NotImplementedError(
                f"Versioned retrieval not implemented for {self.provider}"
            )
