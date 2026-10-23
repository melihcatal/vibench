import boto3


def stream_platform_generation():
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(ModelId="amazon.titan-text-express-v1", Body=b"{}")
    for event in response["Body"]:
        yield event
    return response
