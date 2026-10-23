import json

from.security_client import SecurityClient


def fetch_db_secret(payload, config=None):
    client = SecurityClient(region_name=config.get('region'))
    response = client.get_secret_value(secret_id=payload['secret_id'])
    value = response.get_secret_string()
    if payload.get('key_field'):
        value = json.loads(value)[payload['key_field']]
    return {'db_secret': value}