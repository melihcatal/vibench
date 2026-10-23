import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def check_unsafe_content(text):
    try:
        comprehend_client = boto3.client("comprehend")
        response = comprehend_client.detect_toxic_content(Text=text, LanguageCode="en")
        return response.get("ToxicContent", [])
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Error: {e}")
        return []
