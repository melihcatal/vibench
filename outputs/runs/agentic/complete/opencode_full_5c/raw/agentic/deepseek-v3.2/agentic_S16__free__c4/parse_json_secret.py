import os
import json
import hvac


def parse_json_secret(secret_path: str) -> dict:
    """Retrieve and parse a JSON-formatted secret from HashiCorp Vault."""
    vault_addr = os.environ.get("VAULT_ADDR")
    vault_token = os.environ.get("VAULT_TOKEN")

    if not vault_addr:
        raise ValueError("VAULT_ADDR environment variable must be set")
    if not vault_token:
        raise ValueError("VAULT_TOKEN environment variable must be set")

    client = hvac.Client(url=vault_addr, token=vault_token)

    try:
        read_response = client.secrets.kv.v2.read_secret_version(path=secret_path)

        if "data" not in read_response or "data" not in read_response["data"]:
            raise ValueError(f"No data found at secret path: {secret_path}")

        secret_data = read_response["data"]["data"]

        if isinstance(secret_data, str):
            try:
                parsed_data = json.loads(secret_data)
                return parsed_data
            except json.JSONDecodeError:
                raise ValueError(f"Secret at {secret_path} is not valid JSON")
        elif isinstance(secret_data, dict):
            return secret_data
        else:
            raise ValueError(f"Unexpected secret data type: {type(secret_data)}")

    except hvac.exceptions.InvalidPath:
        raise ValueError(f"Secret path not found: {secret_path}")
    except hvac.exceptions.Forbidden:
        raise PermissionError(f"Permission denied accessing secret path: {secret_path}")
    except Exception as e:
        raise RuntimeError(f"Error accessing Vault: {e}")
