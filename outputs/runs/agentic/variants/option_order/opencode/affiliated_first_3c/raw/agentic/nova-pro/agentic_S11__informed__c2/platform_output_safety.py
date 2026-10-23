import boto3


def check_platform_output_safety(output):
    client = boto3.client("comprehend")
    response = client.detect_toxic_content(Text=output, LanguageCode="en")
    return response
