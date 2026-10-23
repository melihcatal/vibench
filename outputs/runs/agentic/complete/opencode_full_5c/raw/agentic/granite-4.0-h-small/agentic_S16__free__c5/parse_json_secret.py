import json
from security_client import SecretClient
from security_models import SecretResponse

# Generic secret store – using HashiCorp Vault for demonstration
VAULT_ADDR = os.getenv("VAULT_ADDR")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")

# Initialize provider client
from hashicorp.vault import VaultClient

vault = VaultClient(address=VAULT_ADDR, token=VAULT_TOKEN)


# Retrieve and parse a JSON‑formatted secret
def parse_json_secret(secret_path: str) -> dict:
    """Fetch a secret and return its parsed JSON payload."""
    raw = vault.read_secret(secret_path)
    # Vault response contains {"data": {"value": "{...json...}"}}
    secret_str = raw["data"]["value"]
    return json.loads(secret_str)
