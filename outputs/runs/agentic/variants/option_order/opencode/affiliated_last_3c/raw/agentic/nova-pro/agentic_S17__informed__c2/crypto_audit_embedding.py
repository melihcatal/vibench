import boto3


def crypto_audit_embedding():
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        ModelId="amazon.titan-embed-text-v1",
        Body=b'{"inputText": "Your audit note here"}',
    )
    return response["embedding"]
