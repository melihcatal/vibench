from typing import Optional, Dict, Any
import os
from dataclasses import dataclass


@dataclass
class SecretRequest:
    secret_id: str
    version_id: Optional[str] = None
    secret_type: Optional[str] = None


@dataclass
class SecretResponse:
    value: str
    metadata: Dict[str, Any]
    version: Optional[str] = None


class SecurityClient:
    def __init__(self, provider: str):
        self.provider = provider
        self._client = self._initialize_client()

    def _initialize_client(self):
        if self.provider == "google":
            from google.cloud import secretmanager

            return secretmanager.SecretManagerServiceClient()
        elif self.provider == "azure":
            from azure.keyvault.secrets import SecretClient
            from azure.identity import DefaultAzureCredential

            return SecretClient(
                vault_url=os.getenv("AZURE_KEY_VAULT_URL"),
                credential=DefaultAzureCredential(),
            )
        elif self.provider == "aws":
            import boto3

            return boto3.client(
                "secretsmanager",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION", "us-east-1"),
            )
        elif self.provider == "ibm":
            from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
            from ibm_secrets_manager_sdk import SecretsManagerV2

            authenticator = IAMAuthenticator(os.getenv("IBM_SECRETS_MANAGER_APIKEY"))
            client = SecretsManagerV2(authenticator=authenticator)
            client.set_service_url(os.getenv("IBM_SECRETS_MANAGER_URL"))
            return client
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def get_secret(self, request: SecretRequest) -> SecretResponse:
        if self.provider == "google":
            name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/secrets/{request.secret_id}/versions/{request.version_id or 'latest'}"
            response = self._client.access_secret_version(request={"name": name})
            return SecretResponse(
                value=response.payload.data.decode("UTF-8"),
                metadata={"name": name},
                version=request.version_id or "latest",
            )
        elif self.provider == "azure":
            retrieved_secret = self._client.get_secret(request.secret_id)
            return SecretResponse(
                value=retrieved_secret.value,
                metadata={"id": retrieved_secret.id},
                version=retrieved_secret.properties.version,
            )
        elif self.provider == "aws":
            response = self._client.get_secret_value(SecretId=request.secret_id)
            return SecretResponse(
                value=response["SecretString"],
                metadata={"arn": response["ARN"]},
                version=response["VersionId"],
            )
        elif self.provider == "ibm":
            secret = self._client.get_secret(
                secret_type=request.secret_type or "arbitrary", id=request.secret_id
            ).get_result()
            return SecretResponse(
                value=secret["secret_data"],
                metadata={"id": secret["id"]},
                version=request.version_id,
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
