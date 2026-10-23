import requests
import os
import json

def parse_json_secret(project, config, secret):
    url = f'https://api.doppler.com/v3/configs/{project}/config/{secret}'
    headers = {
        'Authorization': f'Bearer {os.getenv(