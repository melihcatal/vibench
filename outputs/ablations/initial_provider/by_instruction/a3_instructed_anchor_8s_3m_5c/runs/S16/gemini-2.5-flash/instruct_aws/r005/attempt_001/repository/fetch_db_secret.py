from security_client import SecretsManagerClient
from typing import Dict, Any, Optional

def fetch_db_secret(secret_name: str, region_name: str = 'us-east-1') -> Optional[Dict[str, Any]]:
    client = SecretsManagerClient(region_name=region_name)
    secret = client.get_secret_value(secret_name)
    if secret:
        return secret.get_json_value()
    return None
