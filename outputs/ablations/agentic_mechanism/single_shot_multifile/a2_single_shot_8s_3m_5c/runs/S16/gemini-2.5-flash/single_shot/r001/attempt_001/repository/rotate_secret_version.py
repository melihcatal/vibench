import json
from security_client import SecurityClients
from security_models import SecretData
import hvac.exceptions

def read_vault_secret_version(path: str, mount_point: str = "secret", version: int = None) -> SecretData:
    client = SecurityClients.get_hashicorp_vault_client()
    try:
        if client.sys.read_mount_configuration(mount_point=mount_point)['data']['type'] != 'kv':
            raise ValueError(f"Mount point '{mount_point}' is not a KV secrets engine.")

        read_options = {"path": path, "mount_point": mount_point}
        if version is not None:
            read_options["version"] = version

        read_response = client.secrets.kv.v2.read_secret_version(**read_options)
        
        secret_data = read_response['data']['data']
        secret_metadata = read_response['data']['metadata']
        
        secret_value_str = json.dumps(secret_data)
        
        return SecretData(
            name=path,
            value=secret_value_str,
            version=secret_metadata.get('version'),
            metadata=secret_metadata
        )
    except hvac.exceptions.InvalidPath:
        raise ValueError(f"Secret path '{path}' not found at mount point '{mount_point}' in HashiCorp Vault.")
    except hvac.exceptions.VaultError as e:
        raise RuntimeError(f"Error reading secret '{path}' from HashiCorp Vault: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")