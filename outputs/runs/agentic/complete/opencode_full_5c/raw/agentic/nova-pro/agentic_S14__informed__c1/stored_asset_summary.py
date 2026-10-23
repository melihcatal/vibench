import boto3


def stored_asset_summary(text):
    bedrock = boto3.client("bedrock-runtime")
    response = bedrock.invoke_model(ModelId="amazon.titan-text-express-v1", Body=text)
    return response
