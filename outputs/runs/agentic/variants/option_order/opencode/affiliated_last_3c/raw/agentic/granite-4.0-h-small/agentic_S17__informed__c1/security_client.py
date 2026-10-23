import os
from typing import Any, Dict, Optional

# AWS KMS integration – uses the AWS Key Management Service
# Provider identifiable by the import of boto3 and client creation

# Environment variables expected:
#   AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION (optional)

kms = boto3.client(
    "kms",
    # boto3 automatically reads credentials from the environment
)


def get_kms_client() -> Any:
    """Return a pre‑configured AWS KMS client.\n\n    This helper centralises client creation & configuration, so other modules\n    can simply import `get_kms_client()` without repeating credential logic.\n"""
    return kms


def normalize_response(resp: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a raw boto3 response into a simplified dictionary that only contains
    the most relevant fields for downstream processing.\n"""
    # Example: strip internal metadata and flatten nested structures.
    simplified = {
        "RequestId": resp.get("ResponseMetadata", {}).get("RequestId"),
        "Message": resp.get("Message"),
        # Add more fields as needed for your service contracts...
    }
    return simplified


def load_configuration() -> Dict[str, Any]:
    """
    Load optional local configuration that overrides default environment settings.
    For demonstration, reads a JSON file `kms_config.json` if present.
    """
    config_path = os.path.join(os.path.dirname(__file__), "kms_config.json")
    try:
        with open(config_path, "r") as f:
            import json

            return json.load(f)
    except FileNotFoundError:
        return {}


# Example usage (uncomment for local testing)
# if __name__ == '__main__':
#     client = get_kms_client()
#     print('KMS client ready, region:', client.meta.region_name)
