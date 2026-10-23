import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError

def get_cloudwatch_client():
    """Return a configured boto3 CloudWatch client, using credentials from environment."""
    region = os.getenv("AWS_REGION", "us-east-1")
    credentials = {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    }
    try:
        client = boto3.client("cloudwatch", region_name=region, **credentials)
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(f"Failed to create CloudWatch client: {exc}")
    return client

if __name__ == "__main__":
    client = get_cloudwatch_client()
    # Simple sanity check: list first 10 metrics.
    metrics = client.list_metrics(Limit=10)
    print(f"Found metrics: {metrics}")
