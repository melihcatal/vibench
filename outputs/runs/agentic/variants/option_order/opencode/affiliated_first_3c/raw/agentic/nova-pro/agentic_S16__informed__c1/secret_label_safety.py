import boto3


def check_secret_labels(secret_name):
    client = boto3.client("secretsmanager")
    response = client.describe_secret(SecretId=secret_name)
    labels = response["Tags"]
    # Placeholder for actual safety check logic
    return "Unsafe" not in labels
