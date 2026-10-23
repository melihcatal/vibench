import boto3


def asset_metadata_embedding(text):
    bedrock = boto3.client("bedrock-runtime")
    response = bedrock.invoke_model(modelId="amazon.titan-embed-text-v1", body=text)
    return response["Body"].read().decode("utf-8")
