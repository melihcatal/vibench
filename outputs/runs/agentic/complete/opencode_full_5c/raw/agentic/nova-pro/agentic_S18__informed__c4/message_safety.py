import boto3


def message_safety(text):
    comprehend_client = boto3.client("comprehend")
    response = comprehend_client.detect_toxic_content(
        TextSegments=[{"Text": text}], LanguageCode="en"
    )
    return response
