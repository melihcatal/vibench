import boto3
import os

class BedrockClient:
    """
    Provides a configured AWS Bedrock client.
    """
    def __init__(self):
        self._client = None

    def get_client(self):
        if self._client is None:
            # AWS Region and credentials can be configured via environment variables
            # AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
            # Or through the AWS CLI configuration
            self._client = boto3.client(
                service_name="bedrock-runtime",
                region_name=os.getenv("AWS_REGION", "us-east-1") # Default to us-east-1 if not set
            )
        return self._client
