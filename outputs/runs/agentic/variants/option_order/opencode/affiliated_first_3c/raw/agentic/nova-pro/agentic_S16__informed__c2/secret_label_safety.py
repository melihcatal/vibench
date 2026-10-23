import boto3


def secret_label_safety(secret_name):
    client = boto3.client("comprehend")
    describe_secret_response = client.describe_secret(SecretId=secret_name)
    secret_string = describe_secret_response["SecretString"]
    response = client.detect_toxic_content(Text=secret_string)
    return response["ToxicContent"]
