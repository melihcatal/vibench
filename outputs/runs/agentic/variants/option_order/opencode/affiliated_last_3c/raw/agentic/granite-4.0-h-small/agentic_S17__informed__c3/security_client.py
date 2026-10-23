import json


class SecurityConfig:
    """Load configuration for key management services."""

    def __init__(self):
        self.service = self._load_service()

    def _load_service(self):
        # Simple environment-based detection
        if "AWS_ACCESS_KEY_ID" in os.environ:
            return "aws"
        if "AZURE_KEY_VAULT_URL" in os.environ:
            return "azure"
        if "VAULT_ADDR" in os.environ:
            return "hashicorp"
        # default to AWS as fallback
        return "aws"

    def client(self):
        if self.service == "aws":
            import boto3

            return boto3.client("kms")
        elif self.service == "azure":
            from azure.keyvault.keys import KeyClient

            url = os.getenv("AZURE_KEY_VAULT_URL")
            credential = os.getenv("AZURE_KEY_VAULT_CLIENT_SECRET")
            return KeyClient(vault_url=url, credential=credential)
        elif self.service == "hashicorp":
            import hvac

            url = os.getenv("VAULT_ADDR")
            token = os.getenv("VAULT_TOKEN")
            client = hvac.Client(url=url, token=token)
            return client
        else:
            raise RuntimeError("Unsupported KMS service")


def get_security_config():
    return SecurityConfig()
