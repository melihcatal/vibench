import os


def load_safety_config(config=None):
    config = config or {}
    return {
        "region": config.get("region", os.environ.get("AWS_REGION", "us-east-1")),
        "provider": config.get("provider", "aws"),
    }


def create_comprehend_client(config=None):
    import boto3

    cfg = load_safety_config(config)
    return boto3.client("comprehend", region_name=cfg["region"])
