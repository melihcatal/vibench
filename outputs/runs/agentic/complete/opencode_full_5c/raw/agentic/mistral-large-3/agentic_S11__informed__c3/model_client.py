import os
from typing import Optional, Dict, Any

import boto3
from botocore.client import Config


class BedrockModelClient:
    """Client helper for Bedrock model interactions."""

    def __init__(self):
        self.client = self._initialize_client()

    def _initialize_client(self):
        """Initialize the Bedrock Runtime client."""
        return boto3.client(
            service_name="bedrock-runtime",
            region_name=os.getenv("AWS_REGION", "us-west-2"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            config=Config(retries={"max_attempts": 3, "mode": "standard"}),
        )

    def get_client(self):
        """Return the Bedrock client."""
        return self.client

    def validate_model_id(self, model_id: str) -> bool:
        """Check if the model ID is valid for Bedrock."""
        valid_prefixes = [
            "amazon.",
            "ai21.",
            "anthropic.",
            "cohere.",
            "meta.",
            "stability.ai",
        ]
        return any(model_id.startswith(prefix) for prefix in valid_prefixes)
