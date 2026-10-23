import boto3


def check_secret_labels_for_unsafe_text(secret_name):
    client = boto3.client("comprehend")
    describe_secret_response = boto3.client("secretsmanager").describe_secret(
        SecretId=secret_name
    )
    labels = (
        describe_secret_response["Name"] + " " + describe_secret_response["Description"]
    )
    result = client.detect_sentiment(Text=labels, LanguageCode="en")
    return result["Sentiment"]
