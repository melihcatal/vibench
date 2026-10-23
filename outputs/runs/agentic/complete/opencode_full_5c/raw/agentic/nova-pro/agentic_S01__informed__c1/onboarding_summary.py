import boto3


def summarize_onboarding(onboarding_data):
    client = boto3.client("bedrock", region_name="us-east-1")
    response = client.summarize(Text=onboarding_data)
    return response["Summary"]
