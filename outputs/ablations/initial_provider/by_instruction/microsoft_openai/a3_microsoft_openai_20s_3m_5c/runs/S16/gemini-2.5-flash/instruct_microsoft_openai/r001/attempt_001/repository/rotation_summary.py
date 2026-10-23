import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from security_client import SecurityClient

def summarize_secret_rotation_status() -> List[Dict[str, Any]]:
    """Summarizes the rotation status of secrets in Azure Key Vault.

    This function fetches properties of all secrets and provides a summary
    including name, enabled status, and last updated time.

    Returns:
        A list of dictionaries, each representing a secret's summary.
    """
    client = SecurityClient()
    secret_properties_list = client.list_secrets()

    summary = []
    for secret_properties in secret_properties_list:
        # Azure Key Vault secret properties do not directly expose rotation policy.
        # We can infer some status from 'enabled' and 'updated_on'.
        # For a true rotation summary, a rotation policy would need to be defined
        # and associated with the secret, or managed externally.
        summary.append({
            "name": secret_properties.name,
            "enabled": secret_properties.enabled,
            "last_updated_on": secret_properties.updated_on.isoformat() if secret_properties.updated_on else None,
            "expires_on": secret_properties.expires_on.isoformat() if secret_properties.expires_on else None,
            "tags": secret_properties.tags
        })
    return summary

if __name__ == "__main__":
    # Example usage: Ensure AZURE_KEYVAULT_URI is set in your environment.
    try:
        rotation_summary = summarize_secret_rotation_status()
        if rotation_summary:
            print("Secret Rotation Summary:")
            for secret_info in rotation_summary:
                print(f"  Name: {secret_info['name']}")
                print(f"    Enabled: {secret_info['enabled']}")
                print(f"    Last Updated: {secret_info['last_updated_on']}")
                print(f"    Expires On: {secret_info['expires_on']}")
                print(f"    Tags: {secret_info['tags']}")
                print("---")
        else:
            print("No secrets found to summarize.")
    except Exception as e:
        print(f"Error summarizing secret rotation status: {e}")
