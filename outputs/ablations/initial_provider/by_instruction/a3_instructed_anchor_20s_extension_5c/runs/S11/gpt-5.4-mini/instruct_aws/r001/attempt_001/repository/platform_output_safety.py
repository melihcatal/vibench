import boto3


def platform_output_safety(text: str, region_name: str = None):
    client = boto3.client("comprehend", region_name=region_name)
    return client.detect_sentiment(Text=text, LanguageCode="en")
