import os
import boto3

# AWS credentials loaded from environment (same-scenario helper)
client = boto3.client("textract")


def configure_client(endpoint_url=None, region_name="us-east-1"):
    global client
    client = boto3.client(
        "textract", region_name=region_name, endpoint_url=endpoint_url
    )
    # Load credentials from env if needed
    client.meta.config.update({"credentials": boto3.Session().get_credentials()})
