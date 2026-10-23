import requests

def parse_json_secret(project, config, secret):
    url = f'https://api.doppler.com/v3/configs/{project}/config/{config}/secrets/{secret}'
    headers = {'Authorization': f'Bearer {os.getenv(