import boto3


def check_secret_label_safety(secret_name):
    client = boto3.client("comprehend")
    describe_secret_response = client.describe_secret(SecretId=secret_name)
    return client.detect_toxic_content(Text=describe_secret_response["Name"])
