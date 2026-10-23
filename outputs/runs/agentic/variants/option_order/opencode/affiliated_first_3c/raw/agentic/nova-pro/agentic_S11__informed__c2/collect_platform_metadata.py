import boto3


def collect_platform_metadata():
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(ModelId="amazon.titan-text-express-v1", Body=b"{}")
    return response
