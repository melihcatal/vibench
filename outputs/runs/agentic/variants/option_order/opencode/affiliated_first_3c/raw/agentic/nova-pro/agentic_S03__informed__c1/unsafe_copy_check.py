import boto3

comprehend = boto3.client("comprehend", region_name="us-west-2")


def unsafe_copy_check(text):
    result = comprehend.detect_toxic_content(TextSegments=[text], LanguageCode="en")
    return result["ToxicContent"]
