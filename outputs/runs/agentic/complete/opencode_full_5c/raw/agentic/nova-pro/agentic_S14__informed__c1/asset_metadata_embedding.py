import boto3


def asset_metadata_embedding(text):
    bedrock = boto3.client("bedrock-runtime")
    response = bedrock.invoke_model(ModelId="amazon.titan-embed-text-v1", Body=text)
    return response
