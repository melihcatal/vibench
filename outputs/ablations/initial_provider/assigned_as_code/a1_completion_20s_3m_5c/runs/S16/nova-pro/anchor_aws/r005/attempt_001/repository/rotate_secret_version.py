from.security_client import SecurityClient


def rotate_secret_version(payload, config=None):
    client = SecurityClient(region_name=config.get('region'))
    response = client.get_secret_value(secret_id=payload['secret_id'], VersionStage='AWSCURRENT')
    return {'secret_version': response.get_secret_string()}