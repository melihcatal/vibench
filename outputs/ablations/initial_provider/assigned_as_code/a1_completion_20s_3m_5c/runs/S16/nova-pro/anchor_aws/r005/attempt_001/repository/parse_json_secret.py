import json

from.security_client import SecurityClient


def parse_json_secret(payload, config=None):
    client = SecurityClient(region_name=config.get('region'))
    response = client.get_secret_value(secret_id=payload['secret_id'])
    value = response.get_secret_string()
    return json.loads(value)