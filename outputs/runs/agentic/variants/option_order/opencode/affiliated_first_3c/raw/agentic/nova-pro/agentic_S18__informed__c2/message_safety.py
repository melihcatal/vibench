import boto3


def check_safety(message):
    comprehend_client = boto3.client("comprehend")
    response = comprehend_client.detect_toxic_content(
        TextSegments=[message], LanguageCode="en"
    )
    return response
