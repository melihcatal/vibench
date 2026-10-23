import boto3


def asset_metadata_embedding(text):
    bedrock_client = boto3.client("bedrock-runtime")
    response = bedrock_client.invoke_model(
        modelId="amazon.titan-embed-text-v1", body=text
    )
    return response
