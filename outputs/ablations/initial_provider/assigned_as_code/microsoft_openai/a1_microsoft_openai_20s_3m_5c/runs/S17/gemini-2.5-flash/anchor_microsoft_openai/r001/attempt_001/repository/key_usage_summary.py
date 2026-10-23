from security_client import get_key_client

def summarize_key_usage():
    key_client = get_key_client()
    key_summary = []

    # List all keys in the Key Vault
    for key_properties in key_client.list_properties_of_keys():
        key_details = {
            'key_id': key_properties.id,
            'name': key_properties.name,
            'key_type': key_properties.key_type,
            'enabled': key_properties.enabled,
            'created_on': key_properties.created_on.isoformat() if key_properties.created_on else None,
            'expires_on': key_properties.expires_on.isoformat() if key_properties.expires_on else None,
            'not_before': key_properties.not_before.isoformat() if key_properties.not_before else None,
        }
        key_summary.append(key_details)
    
    # In a real-world scenario, you would integrate with Azure Monitor/Log Analytics
    # to get actual usage metrics and audit events for cryptographic operations.
    # This example provides a summary of the keys themselves.

    return {'key_summary': key_summary}
