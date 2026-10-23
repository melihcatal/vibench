import boto3
from botocore.exceptions import ClientError


def payload_safety(decrypted_text):
    client = boto3.client("comprehend")
    try:
        response = client.detect_toxic_content(Text=decrypted_text, LanguageCode="en")
        return response["Labels"]
    except ClientError as e:
        print(e)
        return None
