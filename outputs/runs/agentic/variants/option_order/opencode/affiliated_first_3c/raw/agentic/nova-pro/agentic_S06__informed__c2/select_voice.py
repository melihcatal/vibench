import boto3

client = boto3.client("polly")


def list_voices():
    response = client.describe_voices()
    return response["Voices"]
