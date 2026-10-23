import json
from security_client import SecretManagerClient

def parse_json_secret(name):
    """Fetch a secret assumed to be JSON and return its parsed object.
    Uses Google Secret Manager via the helper client.
    """
    client = SecretManagerClient()
    raw = client.get_secret(name)
    return json.loads(raw)
