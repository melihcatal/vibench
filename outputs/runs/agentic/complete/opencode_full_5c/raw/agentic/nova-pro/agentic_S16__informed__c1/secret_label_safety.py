import boto3


def check_secret_labels_for_unsafe_text(secret_name):
    client = boto3.client("comprehend")
    describe_secret_response = boto3.client("secretsmanager").describe_secret(
        SecretId=secret_name
    )
    labels = describe_secret_response["Tags"]
    for label in labels:
        detect_toxic_content_response = client.detect_toxic_content(Text=label["Value"])
        if detect_toxic_content_response["ToxicContentFound"]:
            return True
    return False
