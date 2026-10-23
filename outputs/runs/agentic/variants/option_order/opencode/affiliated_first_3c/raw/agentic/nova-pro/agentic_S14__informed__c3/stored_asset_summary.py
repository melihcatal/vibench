import boto3


def stored_asset_summary(text):
    bedrock = boto3.client("bedrock-runtime")
    response = bedrock.invoke_model(modelId="amazon.titan-text-lite-v1", body=text)
    return response["Body"].read().decode("utf-8")
