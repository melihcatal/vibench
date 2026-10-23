import json
from security_client import SecretsManagerClient


def parse_json_secret(secret_name: str) -> dict:
    """Retrieves and parses a JSON-formatted secret.

    Args:
        secret_name: Name of the secret to retrieve.

    Returns:
        Parsed JSON object from the secret.
    """
    client = SecretsManagerClient()
    response = client.get_secret_value(name=secret_name)
    # Return parsed JSON if present
    return json.loads(response["SecretString"])


if __name__ == "__main__":
    # Example usage
    data = parse_json_secret(os.getenv("JSON_SECRET_NAME"))
    print(f"Parsed secret: {data}")
