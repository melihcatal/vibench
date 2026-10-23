import os
from typing import List, Dict
from ibm_botocore.client import Config
import ibm_boto3
from ibm_botocore.exceptions import ClientError


class IBMCloudObjectLister:
    """
    Lists stored objects under a bucket or container prefix in IBM Cloud Object Storage.
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

    def list_objects(
        self, bucket_name: str, prefix: str = "", max_keys: int = 1000
    ) -> List[Dict]:
        """
        Lists objects under a prefix in IBM Cloud Object Storage.

        Args:
            bucket_name: Name of the bucket.
            prefix: Prefix to filter objects.
            max_keys: Maximum number of keys to return.

        Returns:
            List[Dict]: List of objects with their metadata.
        """
        try:
            response = self.client.list_objects_v2(
                Bucket=bucket_name, Prefix=prefix, MaxKeys=max_keys
            )

            objects = []
            for obj in response.get("Contents", []):
                objects.append(
                    {
                        "key": obj.get("Key"),
                        "size": obj.get("Size"),
                        "last_modified": obj.get("LastModified"),
                        "etag": obj.get("ETag"),
                        "storage_class": obj.get("StorageClass"),
                    }
                )
            return objects
        except ClientError as e:
            raise Exception(f"Failed to list objects: {e}")
