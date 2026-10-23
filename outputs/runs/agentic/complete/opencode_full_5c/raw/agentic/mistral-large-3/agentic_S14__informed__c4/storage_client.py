import os
from typing import Optional, Union, IO
from ibm_botocore.client import Config
import ibm_boto3


class IBMCloudStorageClient:
    """
    Client helper for IBM Cloud Object Storage.
    """

    def __init__(self):
        self.cos_endpoint = os.getenv("IBM_COS_ENDPOINT")
        self.cos_apikey = os.getenv("IBM_COS_APIKEY")
        self.cos_instance_crn = os.getenv("IBM_COS_INSTANCE_CRN")

        if not all([self.cos_endpoint, self.cos_apikey, self.cos_instance_crn]):
            raise ValueError("IBM Cloud Object Storage credentials not configured.")

        self.client = ibm_boto3.client(
            "s3",
            endpoint_url=self.cos_endpoint,
            aws_access_key_id=self.cos_apikey,
            aws_secret_access_key=self.cos_instance_crn,
            config=Config(signature_version="oauth"),
        )

    def get_client(self):
        """Returns the IBM COS client."""
        return self.client

    def get_bucket_location(self, bucket_name: str) -> str:
        """Returns the location of a bucket."""
        response = self.client.get_bucket_location(Bucket=bucket_name)
        return response.get("LocationConstraint")
