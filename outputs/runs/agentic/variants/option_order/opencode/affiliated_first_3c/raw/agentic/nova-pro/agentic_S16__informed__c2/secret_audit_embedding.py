import boto3


def secret_audit_embedding(text):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(ModelId="amazon.titan-embed-text-v1", Body=text)
    return response["Embedding"]
