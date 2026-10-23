from boto3 import client


def crypto_audit_embedding(text):
    bedrock_client = client("bedrock-runtime")
    response = bedrock_client.invoke_model(
        ModelId="amazon.titan-embed-text-v1", Body=text
    )
    return response["Embedding"]
