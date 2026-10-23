import os
from ibmcloudant import CloudantClient


class DatabaseClient:
    """Local helper to configure and provide a Cloudant document store client."""

    def __init__(self):
        self.url = os.getenv("IBM_CLOUDANT_URL")
        self.apikey = os.getenv("IBM_CLOUDANT_APIKEY")
        self.client = CloudantClient(url=self.url, auth=self.apikey)

    def get_client(self):
        return self.client
