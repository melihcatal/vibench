import os

class SecurityClientConfig:
    """
    Local configuration utility for secret management clients.
    """
    def __init__(self):
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.gcp_project_id = os.getenv("GCP_PROJECT_ID")
        self.azure_key_vault_url = os.getenv("AZURE_KEY_VAULT_URL")
        self.vault_addr = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
        self.vault_token = os.getenv("VAULT_TOKEN")
        self.datadog_api_key = os.getenv("DD_API_KEY")
        self.datadog_app_key = os.getenv("DD_APP_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

    def get_aws_config(self):
        return {"region_name": self.aws_region}

    def get_gcp_project_id(self):
        if not self.gcp_project_id:
            raise ValueError("GCP_PROJECT_ID not set in environment variables.")
        return self.gcp_project_id

    def get_azure_key_vault_url(self):
        if not self.azure_key_vault_url:
            raise ValueError("AZURE_KEY_VAULT_URL not set in environment variables.")
        return self.azure_key_vault_url

    def get_vault_config(self):
        if not self.vault_token:
            raise ValueError("VAULT_TOKEN not set in environment variables.")
        return {"vault_addr": self.vault_addr, "token": self.vault_token}

    def get_datadog_config(self):
        if not self.datadog_api_key or not self.datadog_app_key:
            raise ValueError("DD_API_KEY and DD_APP_KEY must be set for Datadog integration.")
        return {"api_key": self.datadog_api_key, "app_key": self.datadog_app_key}

    def get_openai_api_key(self):
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not set in environment variables.")
        return self.openai_api_key

class SecurityClient:
    """
    A placeholder for a composite security client or for individual client instances.
    """
    def __init__(self, config: SecurityClientConfig):
        self.config = config

    # In a full implementation, this might hold initialized provider clients
    # e.g., self.aws_secrets_manager_client = boto3.client('secretsmanager', **config.get_aws_config())
    # self.gcp_secret_manager_client = secretmanager_v1.SecretManagerServiceClient()
    pass
