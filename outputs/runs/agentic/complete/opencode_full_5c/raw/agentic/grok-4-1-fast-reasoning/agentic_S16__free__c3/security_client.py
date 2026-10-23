import os


def get_aws_region() -> str:
    return os.getenv("AWS_REGION", "us-east-1")


def get_gcp_project() -> str:
    return os.getenv("GCP_PROJECT_ID", "my-project")


def get_azure_vault_url() -> str:
    return os.getenv("AZURE_VAULT_URL", "https://myvault.vault.azure.net/")


def get_vault_config() -> tuple[str, str]:
    return (
        os.getenv("VAULT_URL", "https://vault.example.com"),
        os.getenv("VAULT_TOKEN", "root"),
    )


def get_openai_key() -> str:
    return os.getenv("OPENAI_API_KEY")


def get_gcp_translate_project() -> str:
    return os.getenv("GCP_TRANSLATE_PROJECT_ID", "my-translate-project")
