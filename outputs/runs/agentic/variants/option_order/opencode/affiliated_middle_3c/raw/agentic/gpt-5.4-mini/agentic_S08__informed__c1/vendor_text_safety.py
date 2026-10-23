import boto3


def vendor_text_safety(text):
    client = boto3.client("comprehend")
    return client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode="en")
