import boto3


def summarize_message(message):
    bedrock_client = boto3.client("bedrock-runtime")
    response = bedrock_client.invoke_model(
        ModelId="amazon.titan-text-express-v1", Body=message
    )
    return response
