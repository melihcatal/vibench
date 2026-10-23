import os
from ibm_botocore.client import Config
import ibm_boto3
from typing import Optional

class StorageClient:
    """Client helper for IBM Cloud Object Storage."""

    def __init__(self):
        self.endpoint = os.getenv("IBM_COS_ENDPOINT")
        self.api_key = os.getenv("IBM_COS_APIKEY")
        self.service_instance_id = os.getenv("IBM_COS_SERVICE_INSTANCE_ID")
        self.client = self._create_client()

    def _create_client(self) -> ibm_boto3.client:
        return ibm_boto3.client(
            service_name="s3",
            ibm_api_key_id=self.api_key,
            ibm_service_instance_id=self.service_instance_id,
            config=Config(signature_version="oauth"),
            endpoint_url=self.endpoint,
        )

    def get_client(self) -> ibm_boto3.client:
        return self.client