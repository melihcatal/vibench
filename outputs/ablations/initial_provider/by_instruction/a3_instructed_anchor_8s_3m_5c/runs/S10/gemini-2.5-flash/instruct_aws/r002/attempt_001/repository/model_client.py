import boto3

class BedrockClient:
    """
    Provides a configured AWS Bedrock runtime client.
    """
    def __init__(self, region_name: str = "us-east-1"):
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=region_name
        )

    def get_client(self):
        return self.client

