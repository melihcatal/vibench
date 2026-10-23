import boto3


def crypto_audit_embedding():
    bedrock_client = boto3.client("bedrock-runtime", region_name="us-west-2")
    response = bedrock_client.invoke_model(
        ModelId="amazon.titan-embed-text-v1", Body=b'{"inputText":"Example audit note"}'
    )
    return response["embedding"]
