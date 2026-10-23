import boto3


def check_secret_label_safety(secret_id):
    client = boto3.client("comprehend")
    response = client.detect_toxic_content(Text=secret_id)
    return response["ToxicContent"]
