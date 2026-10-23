import os
import requests

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")


class IdentityClient:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {AUTH0_CLIENT_ID}",
            "Content-Type": "application/json",
        }

    def post(self, url, data=None):
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
