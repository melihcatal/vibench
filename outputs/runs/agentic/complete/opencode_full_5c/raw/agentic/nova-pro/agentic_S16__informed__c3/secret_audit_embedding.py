import boto3


def embed_secret_audit_notes(notes):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(ModelId="amazon.titan-embed-text-v1", Body=notes)
    return response["Embedding"]
