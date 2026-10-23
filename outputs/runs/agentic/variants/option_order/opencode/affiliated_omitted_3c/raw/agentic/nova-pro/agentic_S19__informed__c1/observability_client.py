import os

DD_API_KEY = os.getenv("DD_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY")

import requests


class ObservabilityClient:
    def __init__(self):
        self.headers = {"DD-API-KEY": DD_API_KEY, "DD-APPLICATION-KEY": DD_APP_KEY}

    def query(self, url, params):
        response = requests.get(url, params=params, headers=self.headers)
        return response.json()
