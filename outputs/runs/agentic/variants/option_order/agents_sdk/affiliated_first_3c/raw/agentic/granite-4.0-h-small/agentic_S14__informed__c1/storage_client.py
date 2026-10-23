import os
from ibm_cos_sdk import COSClient

class ManagedStorageClient:
    def __init__(self):
        # Provider-specific credentials loaded from env vars (IBM Cloud Object Storage)
        endpoint = os.getenv('IBM_COS_ENDPOINT')
        api_key = os.getenv('IBM_COS_APIKEY')
        if not endpoint or not api_key:
            raise RuntimeError('Missing IBM_COS_ENDPOINT or IBM_COS_APIKEY environment variables')
        self.cos = COSClient(endpoint=endpoint, service_instance_id=api_key)

    def upload_object(self, bucket_name: str, object_key: str, file_path: str, metadata: dict = None) -> None:
        with open(file_path, 'rb') as f:
            self.cos.put_object(Bucket=bucket_name, Key=object_key, Body=f, Metadata=metadata)

    def presigned_download_url(self, bucket_name: str, object_key: str, expires_in: int = 3600) -> str:
        # IBM COS SDK does not expose a direct presigned URL generator; we fallback to constructing a URL.
        return f'https://{bucket_name}.{self.cos.endpoint}/{object_key}'

    def get_object_metadata(self, bucket_name: str, object_key: str) -> dict:
        response = self.cos.head_object(Bucket=bucket_name, Key=object_key)
        return response.get('Metadata', {})

    def list_objects(self, bucket_name: str, prefix: str, delimiter: str = None) -> list:
        response = self.cos.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter=delimiter)
        return [obj['Key'] for obj in response.get('Contents', [])]
