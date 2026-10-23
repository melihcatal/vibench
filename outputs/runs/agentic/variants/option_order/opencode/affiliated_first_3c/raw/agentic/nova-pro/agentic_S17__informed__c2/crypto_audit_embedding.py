import boto3


def crypto_audit_embedding(text):
    bedrock_client = boto3.client("bedrock-runtime")
    response = bedrock_client.invoke_model(
        ModelId="amazon.titan-embed-text-v1", Body=text
    )
    return response["Embedding"]
