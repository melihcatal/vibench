import os
import boto3

class AwsMessagingClient:
    """
    Provides initialized Boto3 clients for AWS SNS and SQS,
    configured with region from environment variables.
    """
    def __init__(self, region_name: str = None):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self._sns_client = None
        self._sqs_client = None

    @property
    def sns_client(self):
        if self._sns_client is None:
            self._sns_client = boto3.client("sns", region_name=self.region_name)
        return self._sns_client

    @property
    def sqs_client(self):
        if self._sqs_client is None:
            self._sqs_client = boto3.client("sqs", region_name=self.region_name)
        return self._sqs_client

if __name__ == "__main__":
    # Example Usage
    # client_factory = AwsMessagingClient()
    # sns = client_factory.sns_client
    # sqs = client_factory.sqs_client
    # print(f"SNS Client: {sns}")
    # print(f"SQS Client: {sqs}")
    pass
