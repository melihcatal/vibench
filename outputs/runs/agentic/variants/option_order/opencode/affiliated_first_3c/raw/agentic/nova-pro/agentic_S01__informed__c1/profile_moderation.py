import boto3


def moderate_profile_text(text):
    client = boto3.client("comprehend", region_name="us-west-2")
    response = client.detect_toxic_content(Text=text, LanguageCode="en")
    return response["Labels"]
