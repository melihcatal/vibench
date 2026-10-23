import boto3


def check_platform_output_safety(output, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region", "us-east-1"))
    response = client.detect_toxic_content(
        Text=output,
        LanguageCode='en'
    )
    return response['Labels']