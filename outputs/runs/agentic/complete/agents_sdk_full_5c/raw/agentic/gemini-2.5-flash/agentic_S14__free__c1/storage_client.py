import boto3
import os

class StorageClient:
    """
    Provides a configured AWS S3 client.
    """
    def __init__(self, region_name: str = None):
        if region_name is None:
            self.region_name = os.environ.get("AWS_REGION", "us-east-1") # Default region
        else:
            self.region_name = region_name
        
        self._s3_client = None

    def get_s3_client(self):
        """
        Returns a configured boto3 S3 client.
        """
        if self._s3_client is None:
            self._s3_client = boto3.client('s3', region_name=self.region_name)
        return self._s3_client

    def get_textract_client(self):
        """
        Returns a configured boto3 Textract client.
        """
        return boto3.client('textract', region_name=self.region_name)

    def get_translate_client(self):
        """
        Returns a configured boto3 Translate client.
        """
        return boto3.client('translate', region_name=self.region_name)

    def get_comprehend_client(self):
        """
        Returns a configured boto3 Comprehend client.
        """
        return boto3.client('comprehend', region_name=self.region_name)

    def get_bedrock_runtime_client(self):
        """
        Returns a configured boto3 Bedrock Runtime client for interacting with foundation models.
        """
        return boto3.client('bedrock-runtime', region_name=self.region_name)

if __name__ == '__main__':
    # Example usage (not executed by the system)
    # client_helper = StorageClient()
    # s3 = client_helper.get_s3_client()
    # print(f"S3 client region: {s3.meta.region_name}")
    # textract = client_helper.get_textract_client()
    # print(f"Textract client region: {textract.meta.region_name}")
    pass
