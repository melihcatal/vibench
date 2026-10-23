import os
from ibm_cos_sdk import ServiceClient


class StorageClient:
    """Local helper utilities for Managed Object Storage.
    Uses IBM Cloud Object Storage SDK for demonstrations.
    """

    def __init__(self):
        # Environment variables for IBM COS authentication
        self.endpoint = os.getenv("IBM_COS_ENDPOINT")
        self.api_key = os.getenv("IBM_COS_APIKEY")
        self.service = ServiceClient(endpoint=self.endpoint, api_key=self.api_key)

    def get_service(self):
        return self.service
