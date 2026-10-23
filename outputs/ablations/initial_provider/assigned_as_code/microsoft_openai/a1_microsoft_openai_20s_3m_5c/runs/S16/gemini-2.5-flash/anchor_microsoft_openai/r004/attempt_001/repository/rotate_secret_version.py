from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def rotate_secret_version(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            secret_name = payload['secret_name']
            version_id = payload.get('version_id')
            
            if version_id:
                # To get a specific version, you usually need to provide the version ID.
                # The get_secret method can take a version parameter.
                secret_bundle = client.get_secret(secret_name, version=version_id)
            else:
                # If no version_id is provided, get the latest version
                secret_bundle = client.get_secret(secret_name)
            
            # In a real rotation, you would likely set a new secret value here.
            # For this scenario, we're focusing on reading a specific version.
            # Example of setting a new secret (commented out as it's not the primary focus of 'read specific version'):
            # if payload.get('new_secret_value'):
            #     client.set_secret(secret_name, payload['new_secret_value'])
            #     return {'message': f'Secret {secret_name} rotated and version {secret_bundle.id} read.', 'value': secret_bundle.value}
            
            return {
                'secret_name': secret_bundle.name,
                'value': secret_bundle.value,
                'version': secret_bundle.id.split('/')[-1] # Extract version from ID
            }
