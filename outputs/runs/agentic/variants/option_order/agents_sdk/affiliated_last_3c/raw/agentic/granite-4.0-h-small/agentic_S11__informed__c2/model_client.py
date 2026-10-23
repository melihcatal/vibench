# model_client.py
"""Local configuration and client helper utilities for Managed Model Platform Workflow.
Provides concrete SDK client factories for the chosen provider (Amazon Bedrock).
"""

import os
import boto3
from botocore.exceptions import NoCredentialsError

class BedrockRuntime:
    """Thin wrapper around boto3's Bedrock Runtime client.

    Retrieves AWS credentials from environment (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
    AWS_REGION) and creates a client ready for invoke_model calls.
    """
    _client = None

    @staticmethod
    def get_client() -> boto3.client:
        """Return a singleton Bedrock Runtime client."""
        if BedrockRuntime._client is None:
            try:
                BedrockRuntime._client = boto3.client(
                    "bedrock-runtime",
                    region_name=os.getenv("AWS_REGION", "us-east-1")
                )
            except NoCredentialsError:
                raise RuntimeError("AWS credentials not found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY.")
        return BedrockRuntime._client

    @staticmethod
def invoke_model(request: dict) -> object:
        """Invoke the selected Bedrock deployment and return the raw SDK response."""
        client = BedrockRuntime.get_client()
        return client.invoke_model(**request)
