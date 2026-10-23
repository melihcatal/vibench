import os
from ibm_botocore.client import Config
import ibm_boto3
from datetime import datetime, timedelta


class IBMCloudPresignedDownloadURLGenerator:
    """
    Generates a time-limited presigned download URL for IBM Cloud Object Storage.
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

    def generate_presigned_download_url(
        self, bucket_name: str, object_key: str, expiration: int = 3600
    ) -> str:
        """
        Generates a presigned URL for downloading an object.

        Args:
            bucket_name: Name of the bucket.
            object_key: Key of the object.
            expiration: Time in seconds for the URL to remain valid.

        Returns:
            str: Presigned download URL.
        """
        try:
            url = self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": object_key},
                ExpiresIn=expiration,
            )
            return url
        except Exception as e:
            raise Exception(f"Failed to generate presigned URL: {e}")
