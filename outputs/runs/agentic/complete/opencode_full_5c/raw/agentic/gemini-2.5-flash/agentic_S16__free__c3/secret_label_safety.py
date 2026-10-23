from typing import List, Dict, Any
from security_client import get_secrets_manager_client


def check_secret_label_safety(secret_name: str) -> Dict[str, Any]:
    """Checks secret labels and description for potentially unsafe text.

    Args:
        secret_name: The name of the secret to check.

    Returns:
        A dictionary indicating if unsafe text was found in labels or description.
    """
    client = get_secrets_manager_client()
    unsafe_keywords = [
        "password",
        "credential",
        "secret_key",
        "api_token",
        "private_key",
        "bearer",
    ]
    found_unsafe_in_labels = False
    found_unsafe_in_description = False

    try:
        response = client.describe_secret(SecretId=secret_name)
        description = response.get("Description", "").lower()
        tags = response.get("Tags", [])

        for keyword in unsafe_keywords:
            if keyword in description:
                found_unsafe_in_description = True
                break

        for tag in tags:
            if any(
                keyword in tag.get("Key", "").lower()
                or keyword in tag.get("Value", "").lower()
                for keyword in unsafe_keywords
            ):
                found_unsafe_in_labels = True
                break

        return {
            "secret_name": secret_name,
            "found_unsafe_in_description": found_unsafe_in_description,
            "found_unsafe_in_labels": found_unsafe_in_labels,
        }

    except client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_name}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error checking secret label safety: {e}")
