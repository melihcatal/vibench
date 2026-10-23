from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def rotation_summary(config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            secrets_summary = []
            for secret_properties in client.list_properties_of_secrets():
                secret_name = secret_properties.name
                # To get more details like enabled, created_on, expires_on, we need to fetch the secret itself or its latest version properties
                # For summary, list_properties_of_secrets gives us some basic info.
                # To get full details per secret, we'd iterate through versions or get the latest secret.
                # For a summary, we'll use the properties from list_properties_of_secrets.
                
                # Note: secret_properties doesn't directly contain 'enabled', 'created_on', 'expires_on' for all versions
                # To get this information, we would typically fetch the latest secret bundle.
                # For simplicity in summary, we'll use available properties.
                secrets_summary.append({
                    'name': secret_name,
                    'enabled': secret_properties.enabled,
                    'expires_on': str(secret_properties.expires_on) if secret_properties.expires_on else 'N/A',
                    'created_on': str(secret_properties.created_on) if secret_properties.created_on else 'N/A',
                    'tags': secret_properties.tags or {}
                })
    return {'secrets_summary': secrets_summary}
