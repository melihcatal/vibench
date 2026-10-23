import boto3


def payload_safety(decrypted_text):
    client = boto3.client("comprehend")
    response = client.detect_toxic_content(Text=decrypted_text, LanguageCode="en")
    return response["Labels"]
