from ibmcloudant import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
from typing import Dict, Any, Optional


class CloudantClient:
    """
    A helper class to manage IBM Cloudant client configuration and utilities.
    """

    def __init__(self):
        self.authenticator = IAMAuthenticator(os.getenv("IBM_CLOUDANT_APIKEY"))
        self.client = CloudantV1(authenticator=self.authenticator)
        self.client.set_service_url(os.getenv("IBM_CLOUDANT_URL"))

    def get_client(self) -> CloudantV1:
        """Returns the configured IBM Cloudant client."""
        return self.client


def load_config() -> Dict[str, str]:
    """
    Loads IBM Cloudant configuration from environment variables.
    """
    return {
        "api_key": os.getenv("IBM_CLOUDANT_APIKEY"),
        "url": os.getenv("IBM_CLOUDANT_URL"),
    }
