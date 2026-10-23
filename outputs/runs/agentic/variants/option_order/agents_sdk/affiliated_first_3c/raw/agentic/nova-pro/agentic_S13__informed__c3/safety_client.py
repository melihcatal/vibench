import os
import requests

PERSPECTIVE_API_KEY = os.getenv('PERSPECTIVE_API_KEY')

def create_client():
    return requests.Session()

def send_request(client, url, payload, headers):
    return client.post(url, json=payload, headers=headers)