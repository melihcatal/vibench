import boto3
from botocore.config import Config

def get_aws_client(service_name: str, region: str):
    """
    Provides a boto3 client with a standardized configuration.
    """
    config = Config(
       retries = {
          'max_attempts': 3,
          'mode': 'standard'
       }
    )
    client = boto3.client(
        service_name,
        region_name=region,
        config=config
    )
    return client

# Other potential helper functions for different providers could go here.
# For example, a helper to initialize an HVAC client for Vault.
# Or a helper to get credentials for Azure.
