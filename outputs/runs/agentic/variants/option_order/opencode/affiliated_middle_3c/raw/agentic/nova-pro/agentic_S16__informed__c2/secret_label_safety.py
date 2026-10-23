import boto3


def check_secret_labels(secret_name):
    client = boto3.client("secretsmanager", region_name="us-west-2")
    response = client.describe_secret(SecretId=secret_name)
    labels = response["Tags"]
    unsafe_labels = [label for label in labels if "unsafe" in label]
    return unsafe_labels
