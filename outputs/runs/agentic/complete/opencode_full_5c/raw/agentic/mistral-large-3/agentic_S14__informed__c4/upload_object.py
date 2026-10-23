import os
from typing import Optional, Union, IO
from ibm_botocore.client import Config
import ibm_boto3
from ibm_botocore.exceptions import ClientError


class IBMCloudObjectStorageUploader:
    """
    Uploads a file or byte stream to IBM Cloud Object Storage.
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

    def upload_object(
        self,
        bucket_name: str,
        object_key: str,
        body: Union[bytes, IO],
        content_type: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """
        Uploads an object to IBM Cloud Object Storage.

        Args:
            bucket_name: Name of the bucket.
            object_key: Key of the object.
            body: File-like object or bytes to upload.
            content_type: MIME type of the object.
            metadata: Metadata to attach to the object.

        Returns:
            dict: Response from IBM COS.
        """
        try:
            extra_args = {}
            if content_type:
                extra_args["ContentType"] = content_type
            if metadata:
                extra_args["Metadata"] = metadata

            response = self.client.put_object(
                Bucket=bucket_name, Key=object_key, Body=body, **extra_args
            )
            return {
                "bucket": bucket_name,
                "key": object_key,
                "etag": response.get("ETag"),
                "version_id": response.get("VersionId"),
            }
        except ClientError as e:
            raise Exception(f"Failed to upload object: {e}")
