import json
from security_client import SecurityClient

def parse_json_secret(secret_name: str) -> dict:
    client = SecurityClient()
    secret = client.get_secret(secret_name)
    if secret.content_type != "application/json":
        # In a real scenario, you might raise an error or try to parse anyway
        pass
    return json.loads(secret.value)
