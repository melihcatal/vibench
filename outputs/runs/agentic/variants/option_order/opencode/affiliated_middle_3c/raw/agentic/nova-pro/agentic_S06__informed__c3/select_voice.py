import boto3

polly_client = boto3.client(
    "polly",
    aws_access_key_id="YOUR_AWS_ACCESS_KEY_ID",
    aws_secret_access_key="YOUR_AWS_SECRET_ACCESS_KEY",
    region_name="us-west-2",
)


def list_voices():
    response = polly_client.describe_voices()
    return response["Voices"]
