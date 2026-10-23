import os
from typing import Any, Dict, Optional


class SecurityClient:
    """Local helper client that abstracts provider‑specific secret store operations."""

    def __init__(self, provider: str):
        self.provider = provider.lower()
        # Simple configuration lookup – in real code you might load environs or a config file
        self._credentials = {
            "azure": os.getenv("AZURE_VAULT_URL"),
            "aws": (os.getenv("AWS_ACCESS_KEY_ID"), os.getenv("AWS_SECRET_ACCESS_KEY")),
            "google": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        }

    def _get_client(self) -> Any:
        if self.provider == "azure":
            from azure.identity import DefaultAzureCredential
            from azure.keyvault.secrets import SecretClient

            credential = DefaultAzureCredential()
            return SecretClient(
                vault_url=self._credentials["azure"], credential=credential
            )
        elif self.provider == "aws":
            import boto3

            return boto3.client(
                "secretsmanager",
                aws_access_key_id=self._credentials["aws"][0],
                aws_secret_access_key=self._credentials["aws"][1],
            )
        elif self.provider == "google":
            from google.cloud import secretmanager

            return secretmanager.SecretManagerServiceClient()
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def get_secret(self, name: str) -> Dict[str, Any]:
        """Retrieve a secret and return its payload as a dict."""
        client = self._get_client()
        # Provider‑specific call extracted here for brevity
        if self.provider == "azure":
            received = client.get_secret(name)
            return json.loads(received.value)
        elif self.provider == "aws":
            resp = client.get_secret_value(SecretId=name)
            # Secrets Manager returns a binary blob; decode and parse JSON
            return json.loads(resp["SecretString"])
        elif self.provider == "google":
            req = secretmanager.AccessSecretVersionRequest(name=name)
            resp = client.access_secret_version(request=req)
            return json.loads(resp.payload.data.decode("UTF-8"))
        else:
            raise RuntimeError("Unhandled provider")

    def create_secret(self, name: str, payload: Dict[str, Any]) -> None:
        """Create a secret with the given payload."""
        client = self._get_client()
        if self.provider == "azure":
            client.set_secret(name, value=json.dumps(payload))
        elif self.provider == "aws":
            client.create_secret(Name=name, SecretString=json.dumps(payload))
        elif self.provider == "google":
            client.create_secret(
                parent=f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}",
                secret_id=name,
                secret={
                    "replication": {"automatic": True},
                    "secret_data": {"data": json.dumps(payload).encode()},
                },
            )
        else:
            raise RuntimeError("Unhandled provider")

    def delete_secret(self, name: str) -> None:
        """Delete a secret."""
        client = self._get_client()
        if self.provider == "azure":
            client.delete_secret(name)
        elif self.provider == "aws":
            client.delete_secret(SecretId=name)
        elif self.provider == "google":
            client.delete_secret(name=name)
        else:
            raise RuntimeError("Unhandled provider")


def supported_providers() -> list[str]:
    """List the provider strings supported by this helper."""
    return ["azure", "aws", "google"]
