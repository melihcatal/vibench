import os
import json
from typing import Any, Dict
from security_client import SecretManagementClient
from security_models import ParsedJsonSecret


def parse_json_secret(secret_id: str) -> Dict[str, Any]:
    client = SecretManagementClient()
    payload = client.get_secret_payload(secret_id=secret_id)
    if payload and payload.data:
        try:
            json_data = json.loads(payload.data.decode("utf-8"))
            return json_data
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON secret for {secret_id}: {e}")
    raise ValueError(f"JSON secret for {secret_id} not found or is empty.")


if __name__ == "__main__":
    # Example usage: Replace 'your-json-secret-id' with your actual secret ID
    # The secret stored in Google Secret Manager should be a valid JSON string.
    # For local testing, you might need to authenticate with `gcloud auth application-default login`
    try:
        json_secret = parse_json_secret("your-json-secret-id")
        print(f"Successfully fetched and parsed JSON Secret: {json_secret}")
        # Example of accessing a key from the parsed JSON
        if "username" in json_secret:
            print(f"Username from secret: {json_secret['username']}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
