import boto3


def get_kms_client():
    return boto3.client("kms", region_name="us-west-2")


def load_config():
    # Implement configuration loading here
    pass
