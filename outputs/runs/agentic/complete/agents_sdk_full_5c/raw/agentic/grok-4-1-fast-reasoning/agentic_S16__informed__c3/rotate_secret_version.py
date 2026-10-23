from security_client import get_doppler_client

def read_secret_version(project: str, config: str, secret_name: str, version_id: str) -> str:
    client = get_doppler_client()
    url = f'https://api.doppler.com/v3/projects/{project}/configs/{config}/secrets'
    params = {'version': version_id}
    resp = client.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    secrets = data['config']['secrets']
    for secret in secrets:
        if secret['name'] == secret_name:
            return secret['value']
    raise ValueError(f'Secret {secret_name} not found in version {version_id}')
