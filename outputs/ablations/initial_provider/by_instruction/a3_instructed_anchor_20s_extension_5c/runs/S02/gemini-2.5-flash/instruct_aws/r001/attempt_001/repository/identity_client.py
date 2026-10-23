import os
import boto3

class IdentityClient:
    """
    Provides client utilities for interacting with AWS Cognito and other identity-related services.
    """
    def __init__(self):
        self.region = os.environ.get("AWS_REGION")
        if not self.region:
            raise ValueError("AWS_REGION environment variable not set.")
        self.cognito_idp_client = boto3.client('cognito-idp', region_name=self.region)

    def get_cognito_idp_client(self):
        return self.cognito_idp_client

    # Add other utility methods as needed, e.g., for parsing config, etc.
