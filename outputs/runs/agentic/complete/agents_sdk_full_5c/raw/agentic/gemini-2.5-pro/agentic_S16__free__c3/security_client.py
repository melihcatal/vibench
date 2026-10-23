import os
import hvac
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

def get_aws_credentials() -> dict:
    """Provides AWS credentials from environment variables."""
    return {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY"),
    }

def get_gcp_credentials():
    """Provides GCP credentials from a service account file."""
    gcp_sa_file = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if gcp_sa_file and os.path.exists(gcp_sa_file):
        return service_account.Credentials.from_service_account_file(gcp_sa_file)
    return None

def get_hvac_client() -> hvac.Client | None:
    """Initializes and returns an authenticated HVAC client."""
    vault_addr = os.environ.get("VAULT_ADDR")
    vault_token = os.environ.get("VAULT_TOKEN")

    if not vault_addr or not vault_token:
        print("VAULT_ADDR and VAULT_TOKEN environment variables are required.")
        return None

    client = hvac.Client(url=vault_addr, token=vault_token)
    if client.is_authenticated():
        return client
    else:
        print("Vault authentication failed.")
        return None

def get_github_token() -> str | None:
    """Retrieves GitHub token from environment."""
    return os.environ.get("GITHUB_TOKEN")

def get_openai_api_key() -> str | None:
    """Retrieves OpenAI API key from environment."""
    return os.environ.get("OPENAI_API_KEY")

def get_cohere_api_key() -> str | None:
    """Retrieves Cohere API key from environment."""
    return os.environ.get("COHERE_API_KEY")

def get_deepl_api_key() -> str | None:
    """Retrieves DeepL API key from environment."""
    return os.environ.get("DEEPL_AUTH_KEY")
