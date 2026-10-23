import os
from ibm_botocore.client import Config
import ibm_boto3
from ibm_botocore.exceptions import ClientError


class IBMCloudObjectMetadataReader:
    """
    Reads metadata or head information from IBM Cloud Object Storage.
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

    def get_object_metadata(self, bucket_name: str, object_key: str) -> dict:
        """
        Retrieves metadata for an object in IBM Cloud Object Storage.

        Args:
            bucket_name: Name of the bucket.
            object_key: Key of the object.

        Returns:
            dict: Object metadata and head information.
        """
        try:
            response = self.client.head_object(Bucket=bucket_name, Key=object_key)
            return {
                "content_type": response.get("ContentType"),
                "content_length": response.get("ContentLength"),
                "etag": response.get("ETag"),
                "last_modified": response.get("LastModified"),
                "metadata": response.get("Metadata", {}),
                "version_id": response.get("VersionId"),
            }
        except ClientError as e:
            raise Exception(f"Failed to retrieve object metadata: {e}")
